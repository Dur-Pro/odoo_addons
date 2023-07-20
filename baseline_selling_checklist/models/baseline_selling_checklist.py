# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    # Home to First
    research_findings = fields.Text(string='Research Findings', help="The information that was gathered when researching this lead.")
    initial_problem = fields.Text(string='Initial Problem', help="The main problem as stated by the suspect during the fit call.")
    wants_to_solve = fields.Boolean(string='Suspect Wants to Solve', help="The suspect has indicated they want to solve the above problem.")
    discovery_mtg_booked = fields.Date(string='Discovery Meeting Booked', help="The confirmed discovery meeting/call date agreed upon. If discovery call was carried out during fit call, set to the date the call was made.")
    # First to second
    confirmed_problems = fields.One2many('crm.lead.confirmed_problem', 'lead_id', "Confirmed Problems", help="Problems that were confirmed during the discovery meeting/call")
    compelling_reasons = fields.Text(string='Compelling Reasons', help="The compelling reason(s) identified by the client to solve this issue.")
    quantification_logic = fields.Text(string='Quantification Logic', help="The words used by the prospect in determining the problem quantification. Can be paraphrased but must have been stated by the prospect.")
    urgency = fields.Boolean(string='Urgency',help="The client has clearly expressed a desire to solve this problem quickly or before a specific date.")
    sob_earned_respect = fields.Boolean(string="Earned the prospect's respect")
    sob_confident = fields.Boolean(string="Displayed true confidence")
    sob_expertise = fields.Boolean(string="Demonstrated expertise")
    sob_different_question = fields.Boolean(string="Asked questions nobody else asked")
    sob_problem_solving = fields.Boolean(string="Demonstrated excellent problem solving")
    sob_quick_relationship = fields.Boolean(string="Quickly developed a relationship")
    sob_likeable = fields.Boolean(string="Exhibited an extremely likeable personality")
    sob_credibility = fields.Boolean(string="Demonstrated credibility")
    sob_reputation = fields.Boolean(string="Suspect noted good reputation")
    sob_challenge = fields.Boolean(string="Pushed back and asked challenging questions")
    sob_diagnostic = fields.Boolean(string="Did a good job diagnosing the problem")
    sob_humility = fields.Boolean(string="Showed humility")
    # Second to Third
    determined_to_solve = fields.Boolean(string="Prospect is determined to solve the problem.")
    ready_to_pay_more = fields. Boolean(string="Prospect is ready to pay more to solve the problem.")
    with_decision_maker = fields.Boolean(string="Discussions are with the decision maker.")
    competitors = fields.Text(string="Known competitors", help="The competitors the client has mentioned considering.")
    positioned_vs_competition = fields.Boolean(string="Well positioned vs competition", help="Have you managed to eliminate the competition or at least be the last to bid?")
    decision_date = fields.Date(string="Decision Date")
    decision_criteria = fields.Text(string="Decision Criteria",help="The criteria the prospect has stated he will use to make his decision")
    # Third to Home
    history_and_capabilities = fields.Boolean(string="Presented relevant history and capabilities")
    value_proposition = fields.Boolean(string="Clearly articulated value proposition")
    appropriate_solution = fields.Boolean(string="Appropriate solution for needs and $", help="Covered all the needs? Adresses the problem? Addresses nice-to-haves? 2:1 value:price ratio?")
    inoffensive_close = fields.Boolean(string="Inoffensive close", help="Do you believe I completely understand your needs? Do you believe we can solve your problem? Do you want our help?")


class CRMLeadConfirmedProblem(models.Model):
    _name = "crm.lead.confirmed_problem"
    _description = "Confirmed problems related to a given opportunity"

    lead_id = fields.Many2one('crm.lead', 'Lead', required=True)
    importance_index = fields.Integer(string='Importance Index', required=True, help="An index of how important the issue is. Lower numbers are more important.")
    name = fields.Char(string='Description', required=True)
    quantification = fields.Float(string='Quantification', help='Annualized quantification as stated by the client.')

