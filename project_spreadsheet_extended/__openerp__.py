# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Project Spreadsheet',
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
    'depends': ['sale','google_docs','report_aeroo_ooo'],
    'init_xml': [],
    'update_xml': [
        'project_spreadsheet.xml',
        'report/aeroo_report.xml'
    ],
    'demo_xml': [
    ],
    'test':[
    ],
    'installable': True,
    'certificate': '',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: