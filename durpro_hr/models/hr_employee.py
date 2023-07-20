from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _get_domain(self):
        return [('category_id', '=', self.env.ref('uom.uom_categ_length').id)]


    waist_size = fields.Float('Waist size', groups="hr.group_hr_user")
    waist_size_uom_id = fields.Many2one('uom.uom',
                                        string='Unit of Measure for Waist Size',
                                        groups="hr.group_hr_user",
                                        domain=_get_domain
                                        )

    leg_length = fields.Float('Leg Length', groups="hr.group_hr_user")
    leg_length_uom_id = fields.Many2one('uom.uom',
                                        string='Unit of Measure for Legs Length',
                                        groups="hr.group_hr_user",
                                        domain=_get_domain
                                        )

    chest_size = fields.Float('Chest Size', groups="hr.group_hr_user")
    chest_size_uom_id = fields.Many2one('uom.uom',
                                        string='Unit of Measure for Chest Size',
                                        groups="hr.group_hr_user",
                                        domain=_get_domain
                                        )

    arm_length = fields.Float('Arm Length', groups="hr.group_hr_user")
    arm_length_uom_id = fields.Many2one('uom.uom',
                                        string='Unit of Measure for Arms Length',
                                        groups="hr.group_hr_user",
                                        domain=_get_domain
                                        )

    shoes_size = fields.Float('Shoes Size', groups="hr.group_hr_user")
    shoes_size_uom_id = fields.Many2one('uom.uom',
                                        string='Unit of Measure for Shoes',
                                        groups="hr.group_hr_user",
                                        domain=_get_domain
                                        )

    hat_size = fields.Float('Head Size', groups="hr.group_hr_user")
    hat_size_uom_id = fields.Many2one('uom.uom',
                                      string='Unit of Measure for Head',
                                      groups="hr.group_hr_user",
                                      domain=_get_domain
                                      )

