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

import time
from collections import defaultdict

from openerp import pooler
from openerp.report import report_sxw

class insurance_followup_print(report_sxw.rml_parse):
    _name = "insurance.followup.print"

    def __init__(self, cr, uid, name, context=None):
        super(insurance_followup_print, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'ids_to_objects': self._ids_to_objects,
            'do_data': self._do_data,
        })

    def _ids_to_objects(self, form):
        all_lines = []
        for line in self.pool.get('insurance.follwup').browse(self.cr, self.uid, form):
                all_lines.append(line)
        return all_lines

    def _do_data(self,form):
        insu_ids = form.get('line_ids')
        res = []
        for ins_line in self.pool.get('insurance_follwup.followup.line').browse(self.cr,self.uid, insu_ids):
            res.append({
                        'decs': ins_line.description, 
                        })
        return res

report_sxw.report_sxw('report.insurance.followup.report',
        'insurance.follwup', 'addons/insurance_followup/report/insurance_followup_print.rml',
        parser=insurance_followup_print)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
