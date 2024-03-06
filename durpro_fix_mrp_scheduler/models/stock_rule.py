from odoo import fields, models, api
import logging

_logger = logging.getLogger()

class StockRule(models.Model):
    _inherit = "stock.rule"

    def run_scheduler(self, use_new_cursor=False, company_id=False):
        if not company_id:
            companies = self.env['res.company'].search([])
            if len(companies) > 1:
                for company in companies:
                    self.run_scheduler(use_new_cursor, company.id)
        return super().run_scheduler(use_new_cursor, company_id)

    @api.model
    def _get_moves_to_assign_domain(self, company_id):
        moves_domain = super()._get_moves_to_assign_domain(company_id)
        try:
            if 'waiting' not in moves_domain[0][2]:
                moves_domain[0][2].append('waiting')
        except IndexError:
            caller = _logger.findCaller()
            _logger.log(f"Failed to add waiting moves to domain in function {caller[2]} at {caller[0]}:{caller[1]}.")
        return moves_domain
