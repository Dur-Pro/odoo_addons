from openupgradelib import openupgrade


def migrate(cr, version):
    openupgrade.logged_query(
        cr,
        """
        DELETE from account_financial_html_report_line
        WHERE code in ('TAX', 'NEPAT', 'NEPBT', 'SHARE_CAPITAL')  
        """,
        skip_no_result=True,
    )
