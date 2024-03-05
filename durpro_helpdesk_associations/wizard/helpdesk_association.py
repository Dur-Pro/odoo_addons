# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HelpdeskTicketAssociation(models.TransientModel):
    _name = 'helpdesk.ticket.associate'
    _description = 'Associate a ticket to another record'

    ticket_id = fields.Many2one('helpdesk.ticket', string='Related Ticket', required=True)
    # we don't use a reference field because we want to restrict the account.move domain to invoices or bills
    associated_record = fields.Selection(selection=[('out_invoice', 'Customer Invoice'),
                                                    ('work_order', 'FSO Work Order'),
                                                    ('lead', 'Lead / Opportunity'),
                                                    ('purchase_order', 'Purchase Order'),
                                                    ('sale_order', 'Sales Order / Quotation'),
                                                    ('in_invoice', 'Vendor Bill')],
                                         string="Associated Model")
    invoice_id = fields.Many2one('account.move', string="Customer Invoice", domain=[('move_type', '=', 'out_invoice')])
    bill_id = fields.Many2one('account.move', string="Vendor Bill", domain=[('move_type', '=', 'in_invoice')])
    lead_id = fields.Many2one('crm.lead', "Lead")
    purchase_order_id = fields.Many2one('purchase.order', 'Purchase Order')
    sale_order_id = fields.Many2one('sale.order', 'Sales Order')

    def action_associate(self):
        if self.associated_record == 'out_invoice':
            if not self.invoice_id:
                raise ValidationError(_("You must select an associated record."))
            self.invoice_id.helpdesk_ticket_id = self.ticket_id
        elif self.associated_record == 'in_invoice':
            if not self.bill_id:
                raise ValidationError(_("You must select an associated record."))
            self.bill_id.helpdesk_ticket_id = self.ticket_id
        elif self.associated_record == 'lead':
            raise UserError(_("Not yet implemented."))
        elif self.associated_record == 'purchase_order':
            if not self.purchase_order_id:
                raise ValidationError(_("You must select an associated record."))
            self.purchase_order_id.helpdesk_ticket_id = self.ticket_id
        elif self.associated_record == 'sale_order':
            if not self.sale_order_id:
                raise ValidationError(_("You must select an associated record."))
            self.sale_order_id.helpdesk_ticket_id = self.ticket_id
        else:
            raise ValidationError(_("You must select an associated record."))
