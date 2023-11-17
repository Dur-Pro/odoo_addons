from . import models
from odoo import models, fields, api, SUPERUSER_ID


def _post_init(cr, registry):
    # do the update via SQL ...
    sql = "update account_move set amount_residual_signed=-amount_residual where amount_residual is not null"
    cr.execute(sql)
