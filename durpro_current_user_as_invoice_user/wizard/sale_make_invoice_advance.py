from odoo import models


class SaleMakeInvoiceAdvance(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice_vals = super()._prepare_invoice_values(order, name, amount, so_line)
        invoice_vals.update({
            'invoice_user_id': self.env.user.id,
            'user_id': self.env.user.id,
        })
        return invoice_vals
