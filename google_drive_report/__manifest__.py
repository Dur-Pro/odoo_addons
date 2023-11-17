{
    'name': 'Google Drive Report Auto-Upload',
    "version": "1.0",
    "author": "Frédérick Capovilla, Libeo",
    'category': 'Extra Tools',
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
    'data': [
        'data/cron.xml',
        'security/ir.model.access.csv',
        'views/google_drive_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [],
    'depends': ['base_setup', 'google_drive'],
    'description': "Automatically upload specific Excel reports to Google Drive."
}
