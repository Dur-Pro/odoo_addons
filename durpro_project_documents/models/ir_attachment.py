from odoo import models, fields, _
from odoo.exceptions import UserError

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    document_ids = fields.One2many('documents.document', 'attachment_id')

    def send_for_signature(self):
        if self.filtered(lambda r: r.mimetype != 'application/pdf'):
            raise UserError(_('Only PDF files can be sent for signature.'))
        rule = self.env.ref('documents_sign.documents_sign_rule_sign_directly')
        if self.res_model in('project.project', 'project.task'):
            project_id = self.res_id if self.res_model == 'project.project' \
                else self.env['project.task'].browse(self.res_id).project_id.id
            return rule.with_context({'project_id': project_id}). \
                create_record(documents=self.mapped('document_ids'))
        else:
            return rule.create_record(documents=self.mapped('document_ids'))
