from odoo import api, fields, models


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    price_recompute_needed = fields.Boolean(compute='_compute_price_recompute_needed')
    calculate_standard_cost = fields.Boolean(related='production_id.calculate_standard_cost')

    @api.depends('production_id.move_finished_ids.product_id.standard_price')
    def _compute_price_recompute_needed(self):
        self.price_recompute_needed = False
        for move in self.production_id.move_finished_ids:
            product = move.product_id
            if product.cost_method == 'standard' and product.tracking == 'none' and move.state not in ('done', 'cancel'):
                action = product.compute_price()
                if isinstance(action, dict) and 'context' in action and 'default_new_price' in action['context']:
                    if action['context']['default_new_price'] != product.standard_price:
                        self.price_recompute_needed = True
                        return

    def recompute_price(self):
        for move in self.production_id.move_finished_ids:
            product = move.product_id
            if product.cost_method == 'standard' and product.tracking == 'none' and move.state not in ('done', 'cancel'):
                if product.cost_method == 'standard':
                    action = product.compute_price()
                    if isinstance(action, dict) and 'context' in action and 'default_new_price' in action['context']:
                        action_model = self.env[action['res_model']]
                        action_model.with_context(active_model='product.product', active_id=product.id).create({
                            'new_price': action['context']['default_new_price'],
                        }).change_price()
        return {'type': 'ir.actions.do_nothing'}

    def do_produce(self):
        if self.calculate_standard_cost:
            self.recompute_price()

        return super(MrpProductProduce, self).do_produce()
