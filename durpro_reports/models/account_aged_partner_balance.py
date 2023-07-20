from odoo import models, api, fields, _


class AccountReport(models.AbstractModel):
    _inherit = 'account.report'
    filter_currency = None

    def _init_filter_currency(self, options, previous_options=None):
        if not self.filter_currency:
            return
        options['currency'] = True
        options['currency_ids'] = previous_options and previous_options.get('currency_ids') or []
        selected_currency_ids = [int(currency) for currency in options['currency_ids']]
        selected_currencies = (selected_currency_ids and self.env['res.currency'].browse(selected_currency_ids)
                               or self.env['res.currency'].search([('active', '=', 'true')]))
        options['selected_currency_ids'] = selected_currencies.mapped('id')

    def get_report_informations(self, options):
        info = super().get_report_informations(options)
        options = info['options']
        if options.get('currency'):
            options['selected_currency_ids'] = [self.env['res.currency'].browse(int(currency)).id for currency in
                                                options['currency_ids']]
        return info

    def _set_context(self, options):
        ctx = super()._set_context(options)
        if options.get('currency_ids'):
            ctx['currency_ids'] = self.env['res.currency'].browse(
                [int(currency) for currency in options['currency_ids']]).mapped("id")
        return ctx

    def _get_options_domain(self, options):
        domain = super()._get_options_domain(options)
        domain += self._get_options_currency_domain(options)
        return domain

    def _get_options_currency_domain(self, options):
        domain = []
        if options.get('currency_ids'):
            currency_ids = [int(currency) for currency in options['currency_ids']]
            domain.append(('report_currency_id', 'in', currency_ids))
        return domain


class ReportAccountAgedReceivable(models.Model):
    _inherit = "account.aged.receivable"
    filter_currency = True


class ReportAccountAgedPayable(models.Model):
    _inherit = "account.aged.payable"
    filter_currency = True
