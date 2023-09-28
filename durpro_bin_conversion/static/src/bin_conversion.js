/** @odoo-module **/

import ListController from 'web.ListController';
import ListView from 'web.ListView';
const viewRegistry = require('web.view_registry');

const ConversionListController = ListController.extend({
    buttons_template: 'durpro_bin_conversion.bin_conversion_buttons',
    events: _.extend({}, ListController.prototype.events, {
        'click .o_button_update_values': '_onUpdateValues',
        'click .o_button_apply_rules': '_onApplyRules',
        'click .o_button_create_locations': '_onCreateLocations',
        'click .o_button_create_putaway_rules': '_onCreatePutawayRules',
    }),
    _onUpdateValues: function () {
        this._rpc({
            model: 'product.bin.conversion',
            method: 'action_update_values',
            args: [],
        }).then(() => {
            this.reload();
        });
    },
    _onApplyRules: function () {
        this._rpc({
            model: 'product.bin.conversion',
            method: 'action_apply_rules_to_available_stock',
            args: [],
        }).then(() => {
            this.reload();
        });
    },
    _onCreateLocations: function () {
        this._rpc({
            model: 'product.bin.conversion',
            method: 'action_create_locations',
            args: [],
        }).then(() => {
            this.reload();
        });
    },
    _onCreatePutawayRules: function () {
        this._rpc({
            model: 'product.bin.conversion',
            method: 'action_create_putaway_rules',
            args: [],
        }).then(() => {
            this.reload();
        });
    },
});

const ConversionListView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Controller: ConversionListController,
    }),
});

viewRegistry.add('bin_conversion_tree', ConversionListView);
