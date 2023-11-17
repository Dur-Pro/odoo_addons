# -*- coding: utf-8 -*-

{
	'name': 'HR Attendance Fix',
	'version': '15.0.0.1',
	'category': 'Human Resources/Attendances',
	"license": "AGPL-3",
	'description': """Fixes a bug where certain employees can"t enter leave requests, expense reports, etc. 
					  due to loading the last_check_in field from hr_attendance.employee (limited to users having 
					  access to private employee data)""",
	'author': 'Bemade Inc.',
	'maintainer': 'Marc Durepos <it@bemade.org>',
	'website': 'http://www.bemade.org',
	'depends': [
		'resource',
		'hr_attendance',
	],
	'data': [],
	'installable': True,
}
