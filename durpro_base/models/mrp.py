from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Override to allow for re-using the same component in later productions
    def _check_sn_uniqueness(self):
        """ Alert the user if the serial number as already been consumed/produced. """
        if self.product_tracking == 'serial' and self.lot_producing_id:
            if self._is_finished_sn_already_produced(self.lot_producing_id):
                pass
                # Code below was originally in this method, but breaks if we re-empty a tank for SDI
                # raise UserError(_('This serial number for product %s has already been produced', self.product_id.name))

        for move in self.move_finished_ids:
            if move.has_tracking != 'serial' or move.product_id == self.product_id:
                continue
            for move_line in move.move_line_ids:
                if self._is_finished_sn_already_produced(move_line.lot_id, excluded_sml=move_line):
                    raise UserError(_('The serial number %(number)s used for byproduct %(product_name)s has already been produced',
                                      number=move_line.lot_id.name, product_name=move_line.product_id.name))
        # Original method has code that prevents using the same component twice ... this is illogical as it can happen
        # quite easily in real life. We just remove the code here.
