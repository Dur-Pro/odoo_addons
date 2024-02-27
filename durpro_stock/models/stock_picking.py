from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _calculate_note(self):
        return self.sale_id.note if self.sale_id else ""

    package_type = fields.Char(
        string='Package type',
        size=32
    )
    net_weight = fields.Float(
        string='Net Weight',
        digits=(12, 1),
        help="Net weight in lbs."
    )
    shipper = fields.Many2one(
        comodel_name='res.partner',
        string='Shipper',
        help="The person who prepared the shipment."
    )
    verifier = fields.Many2one(
        comodel_name='res.partner',
        string='Verifier',
        help="The person who verified the shipment."
    )
    carrier = fields.Char(
        string='Carrier (OLD)',
        size=64
    )
    carrier_account = fields.Char(
        string='Carrier Account (OLD)',
        size=64
    )
    printed = fields.Boolean(
        string='Printed',
        help="Indicates whether this picking has been printed already."
    )
    shipping_cost = fields.Float(
        string='Shipping Cost (OLD)',
        digits=(7, 2),
        help="Total cost of this shipment in Canadian Dollars"
    )
    promised_date = fields.Date(
        string='Promised Date',
        help="Delivery date initially promised to the client."
    )
    expected_date = fields.Date(
        string='Expected Ship Date',
        help="Expected delivery date based on promised dates from suppliers."
    )
    note = fields.Html(
        string='Notes',
        default=_calculate_note
    )
    display_name = fields.Char(
        compute="_compute_display_name",
        compute_sudo=True,
    )
    items_summary = fields.Char("Items Summary", compute="_compute_items_summary")

    @api.depends('move_line_ids')
    def _compute_items_summary(self):
        for rec in self:
            rec.items_summary = ""
            for index, line in enumerate(rec.move_lines):
                rec.items_summary += str(round(line.product_qty)) + "x " + (line.product_id.default_code or "")
                if index < len(rec.move_lines) - 1:
                    rec.items_summary += ", "
                if index > 4:
                    rec.items_summary += " ..."

    def _compute_display_name(self):
        for rec in self:
            commercial_partner = rec.partner_id and rec.partner_id.commercial_partner_id
            summary_string = f" - ({rec.items_summary})" if rec.items_summary else ""
            partner_string = f" - ({commercial_partner.name})" if commercial_partner else ""
            rec.display_name = f"{rec.name}{partner_string}{summary_string}"
