# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _


class CreateFSO(models.TransientModel):
    _name = 'helpdesk.create.fso'
    _description = 'Create a Field Service Order'

    helpdesk_ticket_id = fields.Many2one('helpdesk.ticket', string='Related ticket', required=True)
    company_id = fields.Many2one(related='helpdesk_ticket_id.company_id')
    name = fields.Char('Title', required=True)
    sale_id = fields.Many2one('sale.order', string="Sale Order", required=True)
    # project_id = fields.Many2one('project.project', string='Project', help='Project in which to create the task', required=True, domain="[('company_id', '=', company_id), ('is_fsm', '=', True)]")
    send_work_order_to = fields.Many2many(comodel_name='res.partner',
                                          relation='fso_send_work_order_partner_rel_wiz',
                                          string="Send work_order to",)
                                          # domain="[('parent_id', '=', customer_id)]")

    send_invoice_to = fields.Many2many(comodel_name='res.partner',
                                       relation='fso_send_invoice_partner_rel_wiz',
                                       string="Send invoice to",)
                                       # domain="[('parent_id', '=', customer_id)]")

    site_contact_ids = fields.Many2many(comodel_name='res.partner',
                                        string="Site Contacts",
                                        relation='fso_site_contact_partner_rel_wiz',)
                                        # domain="[('parent_id', '=', customer_id), ('is_site_contact', '=', 'True')]")

    @api.model
    def default_get(self, fields_list):
        defaults = super(CreateFSO, self).default_get(fields_list)
        partner_id = defaults.get('partner_id')
        if partner_id:
            delivery = self.env['res.partner'].browse(partner_id).address_get(['delivery']).get('delivery')
            if delivery:
                defaults.update({'partner_id': delivery})
        return defaults

    def _generate_fso_values(self):
        self.ensure_one()
        return {
            'name': self.name,
            'helpdesk_ticket_id': self.helpdesk_ticket_id.id,
            'partner_id': self.sale_id.partner_id.id,
            'sale_id': self.sale_id.id,
            'send_work_order_to': self.send_work_order_to,
            'send_invoice_to': self.send_invoice_to,
            'site_contact_ids': self.site_contact_ids,
        }

    def action_generate_fso(self):
        self.ensure_one()
        return self.env['durpro_fso.work_order'].create(self._generate_fso_values())

    def action_generate_and_view_fso(self):
        self.ensure_one()
        new_fso = self.action_generate_fso()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Field Service Work Order from Tickets'),
            'res_model': 'durpro_fso.work_order',
            'res_id': new_fso.id,
            'view_mode': 'form',
            'view_id': self.env.ref('durpro_fso.work_order_view_form').id,
            'context': {
                'fso_mode': True,
            }
        }
