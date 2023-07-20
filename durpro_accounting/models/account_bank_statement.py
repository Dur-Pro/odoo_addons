from odoo import models, fields, api, _


class AccountBankStatement(models.Model):
    _name = "account.bank.statement"
    _inherit = ["account.bank.statement", "mail.activity.mixin"]
