{
    'name': 'Extended Sales Report',
    'version': '0.1',
    'category': 'Tools',
    'description': """
         Project Spreadsheet Calculation Sale Price. 
         
         * Authenticate with google 
           Setting / user / Syncronization.
         * Give Spreadsheet title in project.
         * Select  project in Sale Order.       
    """,
    'author': 'OpenERP SA',
    'website': 'http://openerp.com',
    'depends': ['project_spreadsheet_extended'],
    'init_xml': [],
    'update_xml': [
        'report/sales_extended_aeroo_report.xml'
    ],
    'demo_xml': [
    ],
    'test':[
    ],
    'installable': True,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
