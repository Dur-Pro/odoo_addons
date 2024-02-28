#
#    Bemade Inc.
#
#    Copyright (C) September 2023 Bemade Inc. (<https://www.bemade.org>).
#    License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).
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
    'name': 'Project Documents',
    'version': '17.0.0.0.1',
    'summary': 'Better document tracking for projects.',
    'category': 'Project/Project',
    'author': 'Bemade Inc.',
    'website': 'https://www.bemade.org',
    'license': 'LGPL-3',
    'depends': ['documents_project',
                'documents_sign',
                ],
    'data': ['views/project_views.xml',
             ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
}
