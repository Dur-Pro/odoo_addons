from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_send_by_email(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """

        self.ensure_one()
        template_id = self.env['ir.model.data']._xmlid_to_res_id('durpro_payment.email_template_payment_notice',
                                                                 raise_if_not_found=True)
        ctx = {
            'default_model': 'account.payment',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_payment_as_sent': True,
            'force_email': True,
            'model_description': self.with_context(lang=self.env.lang).type_name,
            'custom_layout': 'mail.mail_notification_light',
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

    def message_post(self, **kwargs):
        if self.env.context.get('mark_payment_as_sent'):
            self.mark_as_sent()
        return super(AccountPayment, self.with_context(
            mail_post_autofollow=self.env.context.get('mail_post_autofollow', True))).message_post(**kwargs)
