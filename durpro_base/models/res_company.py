from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    sdi_installation_message = fields.Text(string='SDI Installation Message', translate=True)
    sdi_installation_included_message = fields.Text(string='SDI Installation Included Message', translate=True)
    report_header = fields.Html(string='Company Tagline',
                                help="Appears by default on the top right corner of your printed documents (report header).",
                                translate=True)
    report_footer = fields.Html(string='Report Footer', translate=True,
                                help="Footer text displayed at the bottom of all reports.")
    company_details = fields.Html(string='Company Details', help="Header text displayed at the top of all reports.",
                                  translate=True)

    global_client_invoice_notes = fields.Html(string="Global Client Invoice Notes",
                                              help="Notes displayed on all client invoices.",
                                              translate=True)

