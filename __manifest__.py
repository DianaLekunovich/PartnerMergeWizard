{
    'name': 'Partner Merge Wizard',
    'version': '1.0',
    'summary': 'Wizard to merge duplicate partner records',
    'description': """
        This module adds a wizard to merge duplicate partner records.
    """,
    'author': 'Your Name',
    'website': 'http://www.example.com',
    'category': 'Customer Relationship Management',
    'depends': ['base', 'sale_management', 'account'],
    'data': [
        'security/security_groups.xml', #optional
        'security/ir.model.access.csv',
        'views/partner_merge_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
