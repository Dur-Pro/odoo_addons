from . import models


def _post_init(cr, registry):
    # do the update via SQL ...
    sql = "update account_move set amount_residual_signed=amount_residual " \
          "where move_type in ('entry','in_invoice','in_receipt','out_refund')"
    cr.execute(sql)
    sql = "update account_move set amount_residual_signed=-amount_residual " \
          "where move_type not in ('entry','in_invoice','in_receipt','out_refund')"
    cr.execute(sql)
