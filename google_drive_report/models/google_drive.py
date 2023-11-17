import logging
import json
import re

import requests
import itertools

from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, UserError
from odoo.tools.translate import _

from odoo.addons.google_account.models.google_service import GOOGLE_TOKEN_ENDPOINT, TIMEOUT
from odoo.addons.web.controllers.main import CSVExport

_logger = logging.getLogger(__name__)


class GoogleDrive(models.Model):
    _name = 'google.drive.report.config'
    _description = "Google Drive report config"

    def upload_report(self):
        for rec in self:
            # Generate Excel report
            fields = rec.ir_exports_id.export_fields
            Model = rec.env[rec.model].with_context(import_compat=False)
            records = Model.search([], offset=0, limit=False, order=False)

            if not Model._is_an_ordinary_table():
                fields = [field for field in fields if field['name'] != 'id']

            field_names = [f['name'] for f in fields]
            import_data = records.export_data(field_names, True).get('datas',[])
            fields_data = rec.fields_info(rec.model, [f['name'] for f in fields])
            columns_headers = [fields_data[val['name']].strip() for val in fields]

            export = CSVExport()
            data = export.from_data(columns_headers, import_data)

            # Send to Google Drive
            rec.last_status = rec.upload_doc(data).content

    def fields_info(self, model, export_fields):
        # Code adapted from file 'addons/web/controllers/main.py' of Odoo
        info = {}
        fields = self.env[model].fields_get()
        if ".id" in export_fields:
            fields['.id'] = fields.get('id', {'string': 'ID'})

        for (base, length), subfields in itertools.groupby(
                sorted(export_fields),
                lambda field: (field.split('/', 1)[0], len(field.split('/', 1)))):
            subfields = list(subfields)
            if length == 2:
                # subfields is a seq of $base/*rest, and not loaded yet
                info.update(self.graft_subfields(
                    fields[base]['relation'], base, fields[base]['string'],
                    subfields
                ))
            elif base in fields:
                info[base] = fields[base]['string']

        return info

    def graft_subfields(self, model, prefix, prefix_string, fields):
        export_fields = [field.split('/', 1)[1] for field in fields]
        return (
            (prefix + '/' + k, prefix_string + '/' + v)
            for k, v in self.fields_info(model, export_fields).items())

    @api.model
    def get_access_token(self, scope=None):
        Config = self.env['ir.config_parameter'].sudo()
        google_drive_refresh_token = Config.get_param('google_drive_refresh_token')
        user_is_admin = self.env['res.users'].browse(self.env.user.id)._is_admin()
        if not google_drive_refresh_token:
            if user_is_admin:
                dummy, action_id = self.env['ir.model.data'].get_object_reference('base_setup', 'action_general_configuration')
                msg = _("You haven't configured 'Authorization Code' generated from google, Please generate and configure it .")
                raise RedirectWarning(msg, action_id, _('Go to the configuration panel'))
            else:
                raise UserError(_("Google Drive is not yet configured. Please contact your administrator."))
        google_drive_client_id = Config.get_param('google_drive_client_id')
        google_drive_client_secret = Config.get_param('google_drive_client_secret')
        #For Getting New Access Token With help of old Refresh Token
        data = {
            'client_id': google_drive_client_id,
            'refresh_token': google_drive_refresh_token,
            'client_secret': google_drive_client_secret,
            'grant_type': "refresh_token",
            'scope': scope or 'https://www.googleapis.com/auth/drive'
        }
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        try:
            req = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, headers=headers, timeout=TIMEOUT)
            req.raise_for_status()
        except requests.HTTPError:
            if user_is_admin:
                dummy, action_id = self.env['ir.model.data'].get_object_reference('base_setup', 'action_general_configuration')
                msg = _("Something went wrong during the token generation. Please request again an authorization code .")
                raise RedirectWarning(msg, action_id, _('Go to the configuration panel'))
            else:
                raise UserError(_("Google Drive is not yet configured. Please contact your administrator."))
        return req.json().get('access_token')

    @api.model
    def upload_doc(self, data):
        access_token = self.get_access_token()

        request_url = "https://www.googleapis.com/upload/drive/v3/files/%s?uploadType=multipart&supportsAllDrives=true" % (
            self.google_drive_resource_id
        )
        headers = {
            "Authorization": "Bearer %s" % access_token
        }
        meta_data = {
            "name": self.name,
            "description": "%s : Report exported from Odoo" % self.name,
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        files = {
            "data": ("metadata", json.dumps(meta_data), "application/json; charset=UTF-8"),
            "file": data,
        }
        return requests.patch(request_url, headers=headers, files=files, timeout=60*10)

    name = fields.Char('Template Name', required=True)
    # BV was ondelete='set null', it retutn : Only 'restrict' and 'cascade' make sense.
    # Trying restrict, might have to change to cascade, but it can be dangerous
    # Well Restrict pass 13.0 but hang in 14.0 with is defined as ondelete='restrict' while having ir.model as comodel,
    # the 'restrict' mode is not supported for this type of field as comodel.  So trying cascade
    model_id = fields.Many2one('ir.model', 'Model', ondelete='cascade', required=True)
    model = fields.Char('Related Model', related='model_id.model', readonly=True)
    # BV same as previous, was ondelete='set null', it retutn : Only 'restrict' and 'cascade' make sense.
    # Trying restrict, might have to change to cascade, but it can be dangerous
    ir_exports_id = fields.Many2one('ir.exports', 'Report configuration (Excel Export)', ondelete='restrict', required=True)
    google_drive_file_url = fields.Char('File URL', required=True)
    google_drive_resource_id = fields.Char('Resource Id', compute='_compute_ressource_id')
    google_drive_client_id = fields.Char('Google Client', compute='_compute_client_id')
    active = fields.Boolean('Active', default=True)
    last_status = fields.Text('Last upload status', readonly=True)

    def _get_key_from_url(self, url):
        word = re.search("(key=|/d/)([A-Za-z0-9-_]+)", url)
        if word:
            return word.group(2)
        return None

    def _compute_ressource_id(self):
        result = {}
        for record in self:
            word = self._get_key_from_url(record.google_drive_file_url)
            if word:
                record.google_drive_resource_id = word
            else:
                raise UserError(_("Please enter a valid Google Document URL."))
        return result

    def _compute_client_id(self):
        google_drive_client_id = self.env['ir.config_parameter'].sudo().get_param('google_drive_client_id')
        for record in self:
            record.google_drive_client_id = google_drive_client_id

    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.model_id:
            self.model = self.model_id.model
        else:
            self.ir_exports_id = False
            self.model = False

    @api.constrains('model_id', 'ir_exports_id')
    def _check_model_id(self):
        if self.ir_exports_id and self.model_id.model != self.ir_exports_id.resource:
            return False
        return True

