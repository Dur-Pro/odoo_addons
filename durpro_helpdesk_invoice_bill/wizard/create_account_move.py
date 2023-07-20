# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreateAccountMove(models.TransientModel):
    _name = 'helpdesk.create.account_move'
    _description = 'Create a Customer Invoice'

    move_type = fields.Selection([('in_invoice', "Bill"), ('out_invoice', 'Invoice')])
    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Related ticket', required=True)
    company_id = fields.Many2one(related='helpdesk_ticket_id.company_id')
    partner_id = fields.Many2one('res.partner', string="Partner")
    sale_id = fields.Many2one('sale.order', string="Sale Order", domain=[('partner_id', '=', partner_id)])
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order", domain=[('partner_id', '=', partner_id)])

    @api.model
    def default_get(self, fields_list):
        defaults = super(CreateAccountMove, self).default_get(fields_list)
        partner_id = defaults['partner_id'] if 'partner_id' in defaults else False
        if partner_id:
            if defaults['move_type'] == 'out_invoice':
                partner = self.env['res.partner'].browse(partner_id)
                if partner:
                    defaults.update({'partner_id': partner})
        return defaults

    def _generate_invoice_values(self):
        self.ensure_one()
        return {
            'helpdesk_ticket_id': self.helpdesk_ticket_id.id,
            'partner_id': self.partner_id.id,
            'name': '/',
            # 'invoice_origin': self.sale_id.name if self.sale_id else False,
            'move_type': 'out_invoice',
        }

    def _generate_bill_values(self):
        self.ensure_one()
        return {
            'helpdesk_ticket_id': self.helpdesk_ticket_id.id,
            'partner_id': self.partner_id.id,
            'invoice_payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
            # 'invoice_origin': self.purchase_id.name if self.purchase_id else False,
            'move_type': 'in_invoice',
            'name': '/',
        }

    def action_generate_invoice(self):
        self.ensure_one()
        return self.env['account.move'].create(self._generate_invoice_values())

    def action_generate_and_view_invoice(self):
        self.ensure_one()
        new_move = self.action_generate_invoice()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice from Tickets'),
            'res_model': 'account.move',
            'res_id': new_move.id,
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
        }

    def action_generate_bill(self):
        self.ensure_one()
        return self.env['account.move'].create(self._generate_bill_values())

    def action_generate_and_view_bill(self):
        self.ensure_one()
        new_move = self.action_generate_bill()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bill from Tickets'),
            'res_model': 'account.move',
            'res_id': new_move.id,
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
        }


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    @api.model
    def _default_ticket_id(self):
        ticket_id = self._context.get('helpdesk_ticket_id')
        if ticket_id:
            return self.env['helpdesk.ticket'].browse(ticket_id)

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Related ticket', default=_default_ticket_id)

    # Nasty rewrite since method depends on active_ids which we can't change
    @api.depends('helpdesk_ticket_id')
    def create_invoices(self):
        if self.helpdesk_ticket_id:
            sale_orders = self.env['sale.order'].browse(self._context.get('sale_id', []))
        else:
            sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                amount, name = self._get_advance_details(order)

                if self.product_id.invoice_policy != 'order' and self.product_id.service_policy not in (
                'ordered_timesheet', 'delivered_manual'):
                    raise UserError(
                        _('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(
                        _("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(
                    lambda r: not order.company_id or r.company_id == order.company_id)
                tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                so_line = sale_line_obj.create(so_line_values)
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super()._prepare_invoice_values(order, name, amount, so_line)
        invoice_vals['helpdesk_ticket_id'] = self.env.context.get('helpdesk_ticket_id')
        return invoice_vals
