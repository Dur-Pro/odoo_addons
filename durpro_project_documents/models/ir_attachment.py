from odoo import models, fields, api


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    document_ids = fields.One2many('documents.document', 'attachment_id')

    def send_for_signature(self):
        rule = self.env.ref('documents_sign.documents_sign_rule_sign_directly')
        return rule.create_record(documents=self.mapped('document_ids'))
