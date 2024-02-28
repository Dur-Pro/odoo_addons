# -*- coding: utf-8 -*-

from odoo import models, fields

class CRMLeadConfirmedProblem(models.Model):
    _name = "crm.lead.confirmed_problem"
    _description = "Confirmed problems related to a given opportunity"

    lead_id = fields.Many2one('crm.lead', 'Lead', required=True)
    importance_index = fields.Integer(string='Importance Index', required=True, help="An index of how important the issue is. Lower numbers are more important.")
    name = fields.Char(string='Description', required=True)
    quantification = fields.Float(string='Quantification', help='Annualized quantification as stated by the client.')

