/** @odoo-module **/

import accountReportsWidget from 'account_reports.account_report';
import M2MFilters from 'durpro_reports.M2MFilters';
import core from 'web.core';
const QWeb = core.qweb;
import Widget from 'web.Widget';
const _t = core._t;


var durproAccountReportsWidget = accountReportsWidget.extend({
    custom_events: {
        'value_changed': function(ev) {
            var self = this;
            self.report_options.partner_ids = ev.data.partner_ids;
            self.report_options.partner_categories = ev.data.partner_categories;
            self.report_options.analytic_accounts = ev.data.analytic_accounts;
            self.report_options.analytic_tags = ev.data.analytic_tags;
            return self.reload().then(function () {
                self.$searchview_buttons.find('.account_partner_filter').click();
                self.$searchview_buttons.find('.account_analytic_filter').click();
            });
        },
        'currency_value_changed': function(ev) {
            var self = this;
                self.report_options.currency_ids = ev.data.currency_ids;
                return self.reload().then(function() {
                    self.$searchview_buttons.find('account_currency_filter').click();
                });
        },
    },
    render_searchview_buttons: function() {
        var self = this
        this._super.apply(this, arguments);
        if (self.report_options.currency) {
            if(!self.M2MFiltersCurrency) {
                var fields = {};
                if('currency_ids' in this.report_options) {
                    fields['currency_ids'] = {
                        label: _t("Currencies"),
                        modelName: 'res.currency',
                        value: this.report_options.currency_ids.map(Number),
                    };
                }
                if (!_.isEmpty(fields)) {
                    self.M2MFiltersCurrency = new M2MFilters(this, fields, 'currency_value_changed');
                    self.M2MFiltersCurrency.appendTo(this.$searchview_buttons.find('.js_account_currency_m2m'));
                }
            } else {
                    self.$searchview_buttons.find('.js_account_currency_m2m').append(this.M2MFiltersCurrency.$el);
            }
        }
    },
});

core.action_registry.add('durpro_account_report', durproAccountReportsWidget);

