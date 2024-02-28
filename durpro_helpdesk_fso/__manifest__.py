# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details
{
    'name': "Helpdesk FSO",
    'summary': "Allow generating fso from ticket",
    'description': """
        Convert helpdesk tickets to field service order.
    """,
    'category': 'Services/Helpdesk',
    'version': '17.0.0.1',
    'depends': [
        'durpro_fso',
        'helpdesk',
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'data/mail_data.xml',
        'views/helpdesk_views.xml',
        # 'views/project_sharing_views.xml',
        'wizard/create_fso_views.xml',
    ],
    # 'demo': ['data/helpdesk_fsm_demo.xml'],
    # 'auto_install': True,
    'license': 'OEEL-1',
}
