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

from openerp.report import report_sxw

class account_move(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(account_move, self).__init__(cr, uid, name, context=context)
        self.account_ids=[]
        self.localcontext.update({
            'time': time,
            'sum_debit': self._sum_debit,
            'sum_credit': self._sum_credit,
        })

    def _sum_debit(self, line_id=False):
        total_debit =0.0
        for line in line_id:
            total_debit=total_debit+line.debit
        return total_debit

    def _sum_credit(self, line_id=False):
        total_credit =0.0
        for line in line_id:
            total_credit=total_credit+line.credit
        return total_credit

report_sxw.report_sxw('report.account.move.report', 'account.move', 'addons/account/report/account_general_entry.rml', parser=account_move, header=False)


