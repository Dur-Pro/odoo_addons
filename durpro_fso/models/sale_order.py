from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    estimate_misc_parts = fields.Monetary(string='Parts Estimate')

    estimate_tax_ids = fields.Many2many('account.tax',
                                        string='Taxes estimate')

    amount_untaxed_with_estimate = fields.Monetary(string="Sub-Total with est.",
                                                   compute="_compute_amount_untaxed_with_estimate",
                                                   store=True)

    amount_tax_with_estimate = fields.Monetary(string="Taxes with est.",
                                               compute="_compute_amount_tax_with_estimate",
                                               store=True)

    amount_total_with_estimate = fields.Monetary(string="Total with est.",
                                                 compute="_compute_amount_total_with_estimate",
                                                 store=True)

    work_order_ids = fields.One2many(comodel_name='durpro_fso.work_order',
                                     inverse_name='sale_id',
                                     string='Work orders')

    work_order_count = fields.Integer(string='# of Work Orders',
                                      compute='_compute_work_order_ids',
                                      readonly=True)

    # partner_id = fields.Many2one(comodel_name='res.partner',
    #                              string='Customer1',
    #                              readonly=True,
    #                              states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    #                              required=True,
    #                              change_default=True,
    #                              index=True,
    #                              domain="[('is_company', '=', True), "
    #                                     "('is_site', '=', False), "
    #                                     "('is_site_contact', '=', False)]",
    #                              track_visibility='always')

    # def copy_data(self, default=None):
    #     if default is None:
    #         default = {}
    #     if 'work_order_ids' not in default:
    #         default['work_order_ids'] = [(0, 0, line.copy_data()[0]) for line in self.work_order_ids]
    #     return super(SaleOrder, self).copy_data(default)

    @api.depends('work_order_ids')
    def _compute_work_order_ids(self):
        for order in self:
            order.work_order_count = len(order.work_order_ids)

    @api.depends('amount_untaxed', 'estimate_misc_parts')
    def _compute_amount_untaxed_with_estimate(self):
        for order in self:
            order.amount_untaxed_with_estimate = order.amount_untaxed + order.estimate_misc_parts

    @api.depends('amount_untaxed_with_estimate', 'estimate_tax_ids')
    def _compute_amount_tax_with_estimate(self):
        for order in self:
            order.amount_tax_with_estimate = sum([
                tax['amount'] for tax in order.estimate_tax_ids.compute_all(order.amount_untaxed_with_estimate)['taxes']
            ])

    @api.depends('amount_untaxed_with_estimate', 'amount_tax_with_estimate')
    def _compute_amount_total_with_estimate(self):
        for order in self:
            order.amount_total_with_estimate = order.amount_untaxed_with_estimate + order.amount_tax_with_estimate

    def action_view_work_orders(self):
        return self._get_action_view_work_order(self.work_order_ids)

    def _get_action_view_work_order(self, work_orders):
        """
        This function returns an action that display existing work orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one work order to show.
        """

        action = self.env["ir.actions.actions"]._for_xml_id("durpro_fso.action_window_work_order")

#        action = self.env["ir.actions.actions"]._for_xml_id("durpro_fso.act_sale_order_2_work_order")

        if len(work_orders) > 1:
            tree_view = [(self.env.ref('durpro_fso.work_order_view_tree').id, 'tree')]

            if 'views' in action:
                action['views'] = tree_view + [(state, view) for state, view in action['views'] if view != 'tree']
            else:
                action['views'] = tree_view
            action['domain'] = [('id', 'in', work_orders.ids)]
        elif len(work_orders) == 1:
            form_view = [(self.env.ref('durpro_fso.work_order_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = work_orders.ids[0]
        else:
            form_view = [(self.env.ref('durpro_fso.work_order_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = work_orders.id

        # Prepare the context.
        action['context'] = dict(
            self._context,
            default_partner_id=self.partner_id.id,
            default_sale_id=self.id)

        return action

