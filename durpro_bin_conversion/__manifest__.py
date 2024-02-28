#
#    Bemade Inc.
#
#    Copyright (C) July 2023 Bemade Inc. (<https://www.bemade.org>).
#    Author: Marc Durepos (Contact : marc@bemade.org)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
{
    'name': 'Convert Bins to Locations',
    'version': '17.0.1.0.0',
    'summary': "Converts Durpro's product bins to inventory locations and moves stock accordingly.",
    'description': """Converts product bin text field into inventory locations and putaway rules. Once bins are 
                      converted, products in the "Candiac Warehouse" location are moved into the newly created stock 
                      locations as appropriate.""",
    'category': 'Invoicing Management',
    'author': 'Bemade Inc.',
    'website': 'https://www.bemade.org',
    'license': 'OPL-1',
    'depends': ['durpro_base',
                'stock',
                ],
    'data': ['security/ir.model.access.csv',
             'views/bin_conversion_views.xml'],
    'assets': {
        'web.assets_qweb': ['durpro_bin_conversion/static/src/bin_conversion.xml'],
        'web.assets_backend': ['durpro_bin_conversion/static/src/bin_conversion.js'],
    },
    'demo': [''],
    'installable': True,
    'auto_install': False,
}
