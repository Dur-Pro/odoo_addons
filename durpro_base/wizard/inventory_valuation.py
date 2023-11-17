from odoo import _, fields, models
import csv
import base64
from io import StringIO

class InventoryValuationWizard(models.TransientModel):
    _name = 'durpro_base.inventory.valuation.wizard'
    _description = 'Inventory Valuation Wizard'

    location = fields.Many2one('stock.location', 'Location', required=True)
    end_date = fields.Date('End Date', default=fields.Date.today(), required=True)

    def generate_csv(self):
        query = """
            SELECT loc_case as bin,
               inbound.product_id as pid,
               product_product.default_code,
               product_template.name,
               product_template.type,
               product_uom.name as uom,
               (select case when inbound.qty is null then 0 else inbound.qty end) - (select case when outbound.qty is null then 0 else outbound.qty end) as yei,
               standard_price.value_float as standard_price,
               standard_price.value_float * ((select case when inbound.qty is null then 0 else inbound.qty end) - (select case when outbound.qty is null then 0 else outbound.qty end)) as value
            FROM (select product_id, sum(product_qty) as qty from stock_move where state = 'done' and date < %s and location_dest_id in (%s) group by product_id) as inbound
               FULL OUTER JOIN (select product_id, sum(product_qty) as qty from stock_move where state = 'done' and date < %s and location_id in (%s) group by product_id) as outbound on inbound.product_id = outbound.product_id
               JOIN product_product on inbound.product_id = product_product.id
               JOIN product_template on product_product.product_tmpl_id = product_template.id
               JOIN product_uom on product_template.uom_id = product_uom.id
               LEFT JOIN ir_property standard_price on standard_price.id = (SELECT id FROM ir_property WHERE name='standard_price' and res_id = ('product.product,' || product_product.id) ORDER BY company_id ASC LIMIT 1)
            WHERE (select case when inbound.qty is null then 0 else inbound.qty end) > (select case when outbound.qty is null then 0 else outbound.qty end) and product_product.active=true
            ORDER BY loc_case, product_product.default_code 
        """
        self.env.cr.execute(query, (self.end_date, self.location.id, self.end_date, self.location.id))
        lines = self.env.cr.dictfetchall()

        buf = StringIO()
        if lines:
            fieldnames = ['bin', 'pid', 'default_code', 'name', 'type', 'uom', 'yei', 'standard_price', 'value']
            writer = csv.DictWriter(buf, fieldnames=fieldnames)
            writer.writeheader()
            for line in lines:
                writer.writerow(line)

        b64 = base64.encodebytes(bytes(buf.getvalue(), encoding='UTF-8'))
        attachment = self.env['ir.attachment'].create({
            'name': 'InventoryValuation.csv',
            'datas': b64,
            'datas_fname': 'InventoryValuation.csv'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s/%s' % (attachment.id, 'InventoryValuation.csv'),
            'target': 'main',
        }

