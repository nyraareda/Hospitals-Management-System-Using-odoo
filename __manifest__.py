# -*- coding: utf-8 -*-
{
    'name': 'iti_mansoura',
    'version': '1.0',
    'author': 'os',
    'summary': 'Short description of your module',
    'description': """
        Long description of your module
    """,
    'category': 'Uncategorized',
    'depends': ['base'],
    'data': [
       'security/ir.model.access.csv',
       'security/res_group.xml',
       'views/hms_patient_view.xml',
       'views/hms_doctor_view.xml',
       'views/hms_department_view.xml',
       'views/crm_custmor_views.xml',
       'reports/iti_patient_template.xml',
        'reports/reports.xml',
    ],
    'demo': [
        # List of demo data files
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}