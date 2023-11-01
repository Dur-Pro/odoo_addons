from odoo import models


class PurchaseAdvancePaymentInv(models.TransientModel):
    _inherit = 'purchase.advance.payment.inv'

    def create_invoices(self):
        """ Override of the fims_purchase_down_payments wizard to allow creation of invoices when lines are invoiced
        based on received quantities but quantities are not received yet. This allows for the flow of receiving bills
        for shipped goods where the goods have not been received yet, entering the bill into the system, and then
        waiting for the goods to arrive before paying the invoice. The vendor bill should show up in "exception" state
        anyway so this is not very dangerous."""

        purchase_orders = self.env['purchase.order'].browse(self._context.get('active_ids', []))

        # We skip the check for no invoiceable lines from the original code since this is already done by Odoo's code.

        if self.advance_payment_method == 'delivered':
            return purchase_orders.with_context({
                'create_bill': True,
                'deduct_down_payment': self.deduct_down_payments
            }).action_create_invoice()
        else:
            return super().create_invoices()
