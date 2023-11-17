from odoo import _, api, models
from odoo.exceptions import ValidationError
import time

class ReportClientAccountStatement(models.AbstractModel):
    _name = "report.durpro_reports.report_client_account_statement"
    _description = "Prints an account statement with overdue invoices for a given client."

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        for partner_id in docids:
            docs.append(self.env['res.partner'].browse(partner_id))
            # Need to check partner parent IDs
            domain = [('commercial_partner_id', '=', partner_id), ('state', '=', 'posted'),
                      ('payment_state', 'in', ('not_paid', 'partial'))]
            invoices = self.env['account.move'].search(domain)
            if not invoices:
                raise ValidationError(_("This partner has no unpaid invoices."))
        return {'doc_ids': docids,
                'doc_model': 'res.partner',
                'docs': docs,
                'invoices': invoices,
                'data': data,
                'date': time.strftime('%Y-%m-%d')
                }
