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
    'depends': ['contacts', 'base', 'sale_management', 'account', 'web'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/partner_merge_wizard_views.xml',
        'views/res_partner_list_button.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'PartnerMergeWizard/static/src/js/merge_contacts_modal.js',
            'PartnerMergeWizard/static/src/js/res_partner_list_controller.js',
            'PartnerMergeWizard/static/src/xml/custom_button.xml',
            'PartnerMergeWizard/static/src/xml/merge_contacts_template.xml',
        ],
        'web.assets_web': [
        ],
        'web.assets_web_lib': [
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
