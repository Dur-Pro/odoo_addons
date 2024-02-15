from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    client_order_ref = fields.Char(tracking=True)
    purpose = fields.Char(string="Purpose", help="What is this sale order for?")
    client_order_ref = fields.Char(string="Client PO #")

    # Override to allow editing
    date_order = fields.Datetime(
        string='Order Date',
        required=True,
        readonly=True,
        index=True,
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)],
            'sale': [('readonly', False)]
        },
        copy=False,
        default=fields.Datetime.now,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders."
    )

    @api.model
    def delete_rule(self):
        if self.env.ref('sale.menu_sale_quotations', raise_if_not_found=False):
            self.env.ref('sale.menu_sale_quotations').unlink()
        if self.env.ref('sale.menu_sale_order', raise_if_not_found=False):
            self.env.ref('sale.menu_sale_order').unlink()

    def action_sale_order_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_confirm(self):
        ref_required = self.env['ir.config_parameter'].sudo().get_param(
            'durpro_sale.require_sale_reference',
            False
        )
        if ref_required and not self.client_order_ref:
            raise ValidationError(_("Customer reference (PO number) is required to confirm an order."))
        else:
            return super(SaleOrder, self).action_confirm()

    def update_sequence_nos(self):
        """ Since sale order lines get added with a simple default sequence of 10, we sometimes want to re-number
        them since Durpro uses the sequence numbers on their printed quotations and orders."""
        for rec in self:
            # Order lines are already well sorted, so we just go ahead and make sure each line has a number higher
            # than the last.
            last_line = None
            for line in rec.order_line:
                if last_line and line.sequence <= last_line.sequence:
                    line.sequence = last_line.sequence+1
                last_line = line
