from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero
from itertools import groupby


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    shipping_policy_request = fields.Selection([('ship_complete', 'Ship Complete'),
                                                ('ship_partial', 'Ship Partial'),
                                                ('special', 'Special, see note')], string="Shipping Policy")
    shipping_timing_request = fields.Selection([('when_ready', 'Ship When Ready'),
                                                ('on_date_requested', 'Ship on Requested Date'),
                                                ('ask_first', 'Request Permission Prior to Shipping')],
                                               string="Shipping Timing")

    def button_approve(self, force=False):
        self.write({'name': self.name.replace('RFQ', 'PO')})
        super(PurchaseOrder, self).button_approve()

    def button_done(self, force=False):
        self.write({'name': self.name.replace('RFQ', 'PO')})
        super(PurchaseOrder, self).button_done()

    def button_cancel(self, force=False):
        self.write({'name': self.name.replace('PO', 'RFQ')})
        super(PurchaseOrder, self).button_cancel()

    def action_create_invoice(self):
        """ Create the invoice associated to the PO.

        Override to allow creation of an invoice even when there are no lines to invoice on the PO (stock hasn't
        yet been received)."""

        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        lines_to_invoice = self.order_line.filtered(lambda line: line.display_type not in ('line_note', 'line_section')
                                                                 and not float_is_zero(line.qty_to_invoice, precision)
                                                                 and not line.is_downpayment)
        if lines_to_invoice:
            return super().action_create_invoice()

        # With no lines to invoice, we will create an invoice that has quantity 0 for all items but where all items
        # from the PO are present.
        # The following code is a copy of the method from purchase/models/purchase.py but with conditions removed
        # for checking if lines are invoiceable.

        # 1) Prepare invoice vals and clean-up the section lines
        invoice_vals_list = []
        sequence = 10
        for order in self:
            order = order.with_company(order.company_id)
            pending_section = None
            # Invoice values.
            invoice_vals = order._prepare_invoice()
            # Invoice line values (keep only necessary sections).
            for line in order.order_line:
                if line.display_type == 'line_section':
                    pending_section = line
                    continue
                if pending_section:
                    line_vals = pending_section._prepare_account_move_line()
                    line_vals.update({'sequence': sequence, 'quantity': line.product_qty})  # Use ordered quantity
                    invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                    sequence += 1
                    pending_section = None
                line_vals = line._prepare_account_move_line()
                line_vals.update({'sequence': sequence, 'quantity': line.product_qty})  # Use ordered quantity
                invoice_vals['invoice_line_ids'].append((0, 0, line_vals))
                sequence += 1
            invoice_vals_list.append(invoice_vals)

        # 2) group by (company_id, partner_id, currency_id) for batch creation
        new_invoice_vals_list = []
        for grouping_keys, invoices in groupby(invoice_vals_list, key=lambda x: (
                x.get('company_id'), x.get('partner_id'), x.get('currency_id'))):
            origins = set()
            payment_refs = set()
            refs = set()
            ref_invoice_vals = None
            for invoice_vals in invoices:
                if not ref_invoice_vals:
                    ref_invoice_vals = invoice_vals
                else:
                    ref_invoice_vals['invoice_line_ids'] += invoice_vals['invoice_line_ids']
                origins.add(invoice_vals['invoice_origin'])
                payment_refs.add(invoice_vals['payment_reference'])
                refs.add(invoice_vals['ref'])
            ref_invoice_vals.update({
                'ref': ', '.join(refs)[:2000],
                'invoice_origin': ', '.join(origins),
                'payment_reference': len(payment_refs) == 1 and payment_refs.pop() or False,
            })
            new_invoice_vals_list.append(ref_invoice_vals)
        invoice_vals_list = new_invoice_vals_list

        # 3) Create invoices.
        moves = self.env['account.move']
        AccountMove = self.env['account.move'].with_context(default_move_type='in_invoice')
        for vals in invoice_vals_list:
            moves |= AccountMove.with_company(vals['company_id']).create(vals)

        # 4) Some moves might actually be refunds: convert them if the total amount is negative
        # We do this after the moves have been created since we need taxes, etc. to know if the total
        # is actually negative or not
        moves.filtered(
            lambda m: m.currency_id.round(m.amount_total) < 0).action_switch_invoice_into_refund_credit_note()

        return self.action_view_invoice(moves)
