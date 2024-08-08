from odoo import models, fields, api, _
from odoo.tools import html_keep_url, is_html_empty


class SaleBlanketOrder(models.Model):
    _inherit = "sale.blanket.order"

    incoterms_id = fields.Many2one(
        "account.incoterms",
        "Incoterm",
        help="International Commercial Terms are a series of predefined commercial"
        " terms used in international transactions.",
    )

    tag_ids = fields.Many2many(
        comodel_name="crm.tag",
        string="Tags",
    )

    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
    )

    purpose = fields.Char(help="What is this order for?")

    # Make note an HTML field like on sales orders and get it the same default
    # Partner-based computes
    note = fields.Html(
        string="Terms and conditions",
        compute="_compute_note",
        store=True,
        readonly=False,
        precompute=True,
    )
    terms_type = fields.Selection(related="company_id.terms_type")

    @api.depends("partner_id")
    def _compute_note(self):
        """Direct copy/paste from sale.order"""
        use_invoice_terms = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("account.use_invoice_terms")
        )
        if not use_invoice_terms:
            return
        for order in self:
            order = order.with_company(order.company_id)
            if order.terms_type == "html" and self.env.company.invoice_terms_html:
                baseurl = html_keep_url(self.env.company.get_base_url() + "/terms")
                context = {"lang": order.partner_id.lang or self.env.user.lang}
                order.note = _("Terms & Conditions: %s", baseurl)
                del context
            elif not is_html_empty(self.env.company.invoice_terms):
                order.note = order.with_context(
                    lang=order.partner_id.lang
                ).env.company.invoice_terms
