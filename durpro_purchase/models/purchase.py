from odoo import api, fields, models


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


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    loc_case = fields.Char(related='product_id.loc_case', readonly=True)