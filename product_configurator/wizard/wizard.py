# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP

NAME_FIELDS = [
    'name_category',
    'name_type',
    'name_subtype',
    'name_variant',
    'name_size',
    'name_connection_type',
    'name_material',
    'name_manufacturer',
    'name_model',
    'name_qty',
]


class Wizard(models.TransientModel):
    _name = 'product_configurator.wizard'
    _description = 'Product configurator wizard'

    @api.constrains('name')
    def name_must_not_exist(self):
        if self.env['product.template'].search_count([('name', '=', self.name)]):
            raise ValidationError(_('This product already exists.'))

    def _get_default_uom_id(self):
        return self.env['uom.uom'].search([], limit=1, order='id').id

    def similar_names(self):
        domain = [('name', 'ilike', getattr(self, f).name) for f in NAME_FIELDS if getattr(self, f)]
        similar_products = self.env['product.template'].search(domain)
        return {
            'name': 'Similar names',
            'domain': [('id', 'in', similar_products.ids)],
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'limit': 10000,
            'target': 'new',
        }

    def similar_codes(self):
        similar_products = self.env['product.template'].search([('default_code', 'ilike', self.default_code)])
        return {
            'name': 'Similar names',
            'domain': [('id', 'in', similar_products.ids)],
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
            'limit': 10000,
            'target': 'new',
        }

    def create_product(self):
        if not self.name:
            raise ValidationError(_('A product name is required.'))
        if self.env['product.template'].search_count([('name', '=', self.name)]):
            raise ValidationError(_('A product with this name already exists.'))

        product = self.env['product.template'].create({
            'name': self.name,
            'categ_id': self.categ_id.id,
            'sale_ok': self.sale_ok,
            'purchase_ok': self.purchase_ok,
            'type': self.type,
            'uom_id': self.uom_id.id,
            'uom_po_id': self.uom_id.id,
            'default_code': self.default_code,
            'route_ids': [(6, 0, self.route_ids.ids)],
            'sale_delay': self.sale_delay,
            'loc_case': self.loc_case,
            'description': self.description,
            'description_sale': self.description_sale,
            'description_purchase': self.description_purchase,
            'sale_line_warn': self.sale_line_warn,
            'sale_line_warn_msg': self.sale_line_warn,
            'purchase_line_warn': self.purchase_line_warn,
            'purchase_line_warn_msg': self.purchase_line_warn,
            'seller_ids': [(6, 0, self.seller_ids.ids)],
        })
        return {
            'view_type': 'form',
            'res_model': 'product.template',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_id': product.id
        }

    @api.model
    def _get_buy_route(self):
        buy_route = self.env.ref('purchase.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route:
            return buy_route.ids
        return []

    @api.depends('name')
    def _on_change_name(self):
        if self.name:
            domain = [('name', 'ilike', getattr(self, f).name) for f in NAME_FIELDS if getattr(self, f)]
            found_count = self.env['product.template'].search_count(domain)
            found_name = self.env['product.template'].search(domain, limit=10)
            self.found_name = [(6, 0, found_name.ids)]
            self.found_name_string = '{} {}'.format(found_count, _('product(s) with similar name found.'))

    @api.depends('default_code')
    def _on_change_default_code(self):
        if self.default_code:
            domain = [('default_code', 'ilike', self.default_code)]
            found_count = self.env['product.template'].search_count(domain)
            found_code = self.env['product.template'].search(domain, limit=10)
            self.found_code = [(6, 0, found_code.ids)]
            self.found_code_string = '{} {}'.format(found_count, _('product(s) with similar code found.'))

    @api.onchange('categ_id')
    def set_default_values(self):
        # TODO Prévoir un reset des valeurs? Danger d'écraser des valeurs entrées par le user... sinon prévoir une
        #  confirmation de type prompt?
        default_values = self.env['product.category.default'].search([('product_category_id', '=', self.categ_id.id)])
        for value in default_values:
            setattr(self, value.field, value.value)

    @api.depends(
        'name_category',
        'name_type',
        'name_subtype',
        'name_variant',
        'name_size',
        'name_connection_type',
        'name_material',
        'name_manufacturer',
        'name_model',
        'name_qty',
        'name_type',
    )
    def compute_name(self):
        name = ''
        for field in NAME_FIELDS:
            if getattr(self, field):
                name = name + getattr(self, field).name + ', '
        self.name = name[:-2]

    name_category = fields.Many2one('product.name', domain=[('level', '=', 'category')], string='Name: category')
    name_type = fields.Many2one('product.name', domain=[('level', '=', 'type')], string='Name: type')
    name_subtype = fields.Many2one('product.name', domain=[('level', '=', 'subtype')], string='Name: subtype')
    name_variant = fields.Many2one('product.name', domain=[('level', '=', 'variant')], string='Name: variant')
    name_size = fields.Many2one('product.name', domain=[('level', '=', 'size')], string='Name: size')
    name_connection_type = fields.Many2one('product.name', domain=[('level', '=', 'connection_type')],
                                           string='Name: connection type')
    name_material = fields.Many2one('product.name', domain=[('level', '=', 'material')], string='Name: material')
    name_manufacturer = fields.Many2one('product.name', domain=[('level', '=', 'manufacturer')],
                                        string='Name: manufacturer')
    name_model = fields.Many2one('product.name', domain=[('level', '=', 'model')], string='Name: model')
    name_qty = fields.Many2one('product.name', domain=[('level', '=', 'qty')], string='Name: quantity')
    name = fields.Char(readonly=True, string='Name', compute='compute_name')
    categ_id = fields.Many2one('product.category', string='Category',
                               default=lambda self: self.env["product.category"].browse(1))
    sale_ok = fields.Boolean(string='Can be sold')
    purchase_ok = fields.Boolean(string='Can be Purchased')
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Stockable Product')
    ], string='Product Type', default='product', required=True, help="""
            Stockable Product: Standard products that can be purchased, used internally and re-sold. Affects inventory and accounting in the normal ways, i.e. shows up in stock and gets accounted for as a sale when sold and an expense when used in production or sold.
            
            Consumable: Used for products we don’t keep in stock ONLY.  Think toilet paper and test kits.  This is NOT for filter cartridges and membranes that we stock and re-sell (see Stockable Product for those).  These products still affect accounting and have to be put in the right stock locations so be very careful when setting them up and using them.  When in doubt, ASK!  Honestly, if any of this is a surprise to you, ask before using this product type.
            
            Service: Used for non-stockable products that can be purchased and sold but not shipped or kept in stock.  Think FEE-TECH-SPEC and its compatriots.  Service products will be accounted for when invoiced for both sales and purchases and are NEVER tied to delivery orders.  This is another case of ASK before using if unsure. 
    """)
    default_code = fields.Char(string='Internal Reference', index=True)
    uom_id = fields.Many2one(
        'uom.uom', string='Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default Unit of Measure used for all stock operation.")
    route_ids = fields.Many2many(
        'stock.route', 'stock_route_product_product_configurator', 'product_id', 'route_id', string='Routes',
        default=lambda self: self._get_buy_route(),
        domain=[('product_selectable', '=', True)],
        help="Depending on the modules installed, this will allow you to define the route of the product: whether it "
             "will be bought, manufactured, MTO/MTS,...")
    sale_delay = fields.Float(
        string='Customer Lead Time', default=42,
        help="The average delay in days between the confirmation of the customer order and the delivery of the "
             "finished products. It's the time you promise to your customers.")
    loc_case = fields.Char(string='Case')
    description = fields.Text(
        string='Description', translate=True,
        help="A precise description of the Product, used only for internal information purposes.")
    description_sale = fields.Text(
        string='Sale Description', translate=True,
        help="A description of the Product that you want to communicate to your customers. "
             "This description will be copied to every Sales Order, Delivery Order and Customer Invoice/Credit Note")
    description_purchase = fields.Text(
        'Purchase Description', translate=True,
        help="A description of the Product that you want to communicate to your vendors. "
             "This description will be copied to every Purchase Order, Receipt and Vendor Bill/Credit Note.")
    seller_ids = fields.Many2many('product.supplierinfo', domain=[('product_tmpl_id', '=', 0)], string='Vendors')
    found_name = fields.Many2many('product.template', string='Similar Products', compute='_on_change_name')
    found_name_string = fields.Char(compute='_on_change_name')
    found_code = fields.Many2many('product.template', string='Similar Products Code', compute='_on_change_default_code')
    found_code_string = fields.Char(compute='_on_change_default_code')
    cat_help = fields.Char(string='Help', related='categ_id.help', readonly=True)
    sale_line_warn = fields.Selection(WARNING_MESSAGE, 'Sales Order Line', help=WARNING_HELP, required=True,
                                      default="no-message")
    sale_line_warn_msg = fields.Text('Message for Sales Order Line')
    purchase_line_warn = fields.Selection(WARNING_MESSAGE, 'Purchase Order Line', help=WARNING_HELP, required=True,
                                          default="no-message")
    purchase_line_warn_msg = fields.Text('Message for Purchase Order Line')
