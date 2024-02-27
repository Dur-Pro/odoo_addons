#
#    Bemade Inc.
#
#    Copyright (C) 2023-June Bemade Inc. (<https://www.bemade.org>).
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
    'name': 'Durpro Purchase Stock',
    'summary': 'Durpro Purchasing-Stock Customizations',
    'version': '15.0.1.0.0',
    'description': '',
    'category': '',
    'author': 'Bemade Inc.',
    'website': 'http://www.bemade.org',
    'license': 'OPL-1',
    'depends': ['durpro_purchase', 'durpro_stock'],
    'data': [
        'views/purchase_view.xml',
        'views/stock_move_views.xml',
    ],
    'assets': {},
    'installable': True,
    'auto_install': True ,
}