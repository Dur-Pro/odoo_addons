import base64
import csv
from datetime import date
from io import StringIO
from odoo import fields, models


class PricelistImportWizard(models.TransientModel):
    _name = 'durpro_base.pricelist.import.wizard'
    _description = 'Price list import Wizard'

    def _get_default_note(self):
        return '{date} {initials}: ({{new_price}}) Updated using pricelist import script'.format(
            date=str(date.today()),
            initials=''.join([u[0].upper() for u in self.env.user.name.split(' ')]),
        )

    supplier_id = fields.Many2one(
        'res.partner', 'Supplier', required=True, domain=[('supplier', '=', 1), ('parent_id', '=', False)]
    )
    data = fields.Binary('File', required=True)

    new_leadtime = fields.Integer('Leatime to use for this supplier', default=28)
    disc_update = fields.Boolean('Update supplier discount?', default=False)
    new_purchasing_notes = fields.Char(
        'Price list identification for purchasing notes?',
        help='Add {new_price} to include the new price in the note.',
        default=_get_default_note
    )

    def import_file(self):
        logfile = StringIO()
        csv_reader = csv.reader(base64.decodestring(self.data).decode('latin-1').splitlines(), dialect=csv.excel_tab)
        next(csv_reader)

        for item in csv_reader:
            default_code = item[0].strip()
            new_default_code = item[1].strip()
            new_supplier_description = item[2].strip()
            new_supplier_price = item[3]
            if self.disc_update:
                new_supplier_discount = item[4]

            # Find the product id
            query = """SELECT product_tmpl_id AS pid FROM product_product
                        WHERE default_code = %s
                            AND active=true
                UNION
                SELECT product_id AS pid FROM product_supplierinfo
                WHERE product_code = %s
                AND product_id IN (SELECT
                    id FROM product_product WHERE active=true);
                    """
            self.env.cr.execute(query, (default_code, default_code))
            rec = self.env.cr.fetchall()
            if len(rec) == 1:
                product_tmpl_id = rec[0][0]
            else:
                logfile.write('Multiple active products with default_code ' + str(default_code) + ' or product not in system.\n')
                continue

            # Find product_supplierinfo if it exists
            suppinfo = self.env['product.supplierinfo'].search([
                ('name', '=', self.supplier_id.id),
                ('product_tmpl_id', '=', product_tmpl_id),
            ])
            if len(suppinfo) == 1:
                suppinfo = suppinfo[0]
                new_note = self.new_purchasing_notes.format(
                    new_price=str(new_supplier_price) + suppinfo.currency_id.name
                )
                values = {
                    'supplier_list_price': new_supplier_price,
                    'product_name': new_supplier_description,
                    'delay': self.new_leadtime,
                    'product_code': new_default_code,
                    'purchasing_notes': new_note + '\n' + (suppinfo.purchasing_notes or ''),
                    'date_updated': date.today(),
                }
                if self.disc_update:
                    values['supplier_discount_percent'] = new_supplier_discount
                suppinfo.write(values)
                logfile.write("Updated price for product " + str(default_code) + "(" + str(new_default_code) + ").\n")
            else:
                logfile.write("Unable to update price for " + str(default_code) + ": " + str(len(suppinfo)) + " records found for this product.\n")
                continue

        # Return log file
        b64 = base64.encodebytes(bytes(logfile.getvalue(), encoding='UTF-8'))
        attachment = self.env['ir.attachment'].create({
            'name': 'pricelist_import_log.txt',
            'datas': b64,
            'datas_fname': 'pricelist_import_log.txt'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s/%s' % (attachment.id, 'pricelist_import_log.txt'),
            'target': 'main',
        }
