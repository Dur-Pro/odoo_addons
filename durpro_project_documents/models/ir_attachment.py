from odoo import models, fields, _
from odoo.exceptions import UserError

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    document_ids = fields.One2many('documents.document', 'attachment_id')

    def send_for_signature(self):
        if self.filtered(lambda r: r.mimetype != 'application/pdf'):
            raise UserError(_('Only PDF files can be sent for signature.'))
        rule = self.env.ref('documents_sign.documents_sign_rule_sign_directly')
        return rule.create_record(documents=self.mapped('document_ids'))
