from odoo import api, models, _
from odoo.exceptions import UserError


class ReportPaymentReceipt(models.AbstractModel):
    _name = "report.durpro_reports.report_payment_receipt"
    _description = "Prints a payment receipt using the applied discount from account_payment_term_discount."

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        tables = []
        for payment_id in docids:
            payment = self.env['account.payment'].browse(payment_id)
            docs.append(payment)
            tables.append(PaymentReceiptTable(payment))
        return {'doc_ids': docids,
                'doc_model': 'account.payment',
                'docs': docs,
                'tables': tables,
                'data': data}


class PaymentReceiptTable:
    def __init__(self, payment):
        self.payment = payment
        self.partials = payment.move_id._get_reconciled_invoices_partials()
        self.invoices = set()
        for partial in self.partials:
            if partial[2].move_id.move_type != 'entry':
                self.invoices.add(partial[2].move_id)
        self._compute_header()
        self._compute_rows()
        self.currency = payment.currency_id

    def _compute_header(self):
        self.header = self.header = ['Invoice Date', 'Invoice Number', 'Invoice Total', 'Amount Paid']
        if any([invoice.discount_taken > 0 for invoice in self.invoices]):
            self.header.insert(3, 'Discount')

    def _compute_rows(self):
        self.rows = []
        for inv in self.invoices:
            invoice_partials = inv._get_reconciled_invoices_partials()
            # if len(invoice_partials) > 1:
            #     raise UserError(_(f"Invoice {inv.ref} has {len(invoice_partials)} reconciled partials. "
            #                       "This is not supposed to happen. Please notify the system administrator."))
            print("Invoice ", inv.ref, " partials: ", invoice_partials)
            payment_amt = invoice_partials[0][1]
            discount = inv.discount_taken if inv.discount_taken else 0
            print("Invoice ", inv.ref, " discount_amt:", discount)
            payment_amt -= discount
            if 'Discount' in self.header:
                self.rows.append([PaymentReceiptTable.ReceiptTableCell(inv.invoice_date, False),
                                  PaymentReceiptTable.ReceiptTableCell(inv.ref, False),
                                  PaymentReceiptTable.ReceiptTableCell(inv.amount_total, True),
                                  PaymentReceiptTable.ReceiptTableCell(discount, True),
                                  PaymentReceiptTable.ReceiptTableCell(payment_amt, True)])
            else:
                self.rows.append([PaymentReceiptTable.ReceiptTableCell(inv.invoice_date, False),
                                  PaymentReceiptTable.ReceiptTableCell(inv.ref, False),
                                  PaymentReceiptTable.ReceiptTableCell(inv.amount_total, True),
                                  PaymentReceiptTable.ReceiptTableCell(payment_amt, True)])

    class ReceiptTableCell:

        def __init__(self, value: str, monetary: bool):
            self.value = value
            self.monetary = monetary

        def __str__(self):
            return str(self.value)
