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


from openerp.osv import fields, osv
from openerp.tools.translate import _
import xlrd
import time
import gdata.spreadsheet.service
import gspread
import openerp.addons.decimal_precision as dp

class sale_order(osv.osv):
    _inherit = 'sale.order'


    def insert(self, cr, uid, ids, context={}):
		street = ''
		partner_name = ''
		project_name = ''
		phone = ''
		tot_fact = 0.0
		res_user = self.pool.get('res.users')
		sale = self.browse(cr,uid,ids)[0]
		username = res_user.browse(cr, uid, uid, context=context).gmail_user
		passwd = res_user.browse(cr, uid, uid, context=context).gmail_password
		title = sale.document
		if title and username and passwd:
			try: 
				c = gspread.Client(auth=(username,passwd))
				c.login()
				a = c.open(title).sheet1
				sqr = sale.squre_meter
				dist = sale.distance
				sale_type = sale.type or ''
				for line in sale.order_line:
					tot_fact += line.time_factor  
				if sale.project_id:
					project_name = sale.project_id.name
				if sale.partner_id:
					partner_name = sale.partner_id.name
					street = sale.partner_id.street or 'NO'
					phone = sale.partner_id.phone or 'NO'
				a.update_cell(12, 2, str(sale.amount_untaxed))
				a.update_cell(3, 2, str(sale.date_order))
				a.update_cell(2, 2, str(sale.name))
				a.update_cell(4, 2, str(project_name))
				a.update_cell(5, 2, str(street))
				a.update_cell(6, 2, str(sale_type))
				a.update_cell(7, 2, str(sqr))
				a.update_cell(8, 2, str(dist))
				a.update_cell(9, 2, str(partner_name))
				a.update_cell(10, 2, str(phone))
			except Exception, e:
				raise osv.except_osv(_('User Error!'), _('Please give correct google username,password and document title.'))
		else:
			raise osv.except_osv(_('User Error!'), _('Please configure gmail with user and give spreadsheet title.'))    

		return True


    def _tot_volume(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for sale in self.browse(cursor, user, ids, context=context):
            tot = 0.0
            for line in sale.order_line:
        		if line.extend_ids:
        			tot += line.extend_ids[0].prod_qty
            if tot:
                res[sale.id] = tot
            else:
                res[sale.id] = 0.0
        return res

    def _avg_volume(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for sale in self.browse(cursor, user, ids, context=context):
            tot = 0.0
            for line in sale.order_line:
        		if line.extend_ids:
        			tot += line.extend_ids[0].prod_qty
            if tot:
                res[sale.id] = tot/len(sale.order_line)
            else:
                res[sale.id] = 0.0
        return res
        
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
        
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    _columns = {
        'tot_volume': fields.function(_tot_volume, string='Total Volume', type='float'),
        'avg_volume': fields.function(_avg_volume, string='Average Volume', type='float'),
        'calculated' : fields.boolean('Amount Calculated'),
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'calculated'], 10),
                'sale.order.line': (_get_order, ['purchase_price','price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['purchase_price', 'price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'calculated'], 10),
                'sale.order.line': (_get_order, ['purchase_price', 'price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The total amount."),
	}

    def write(self, cr, uid, ids, vals, context=None):
        for rec in self.browse(cr, uid, ids, context=context):
            if vals.get('factor', False): 
                if (rec.factor or 0.0) != vals['factor']:
                    vals.update({'calculated' : False})
            if vals.get('labor_factor', False):
                if (rec.labor_factor or 0.0) != vals['labor_factor']:
                    vals.update({'calculated' : False})
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)
        
	
    def button_calculate(self, cr, uid, ids, context={}):
		order = self.browse(cr,uid,ids[0])
		doc_title = ''
		username = ''
		passwd = ''
		sale_ids = ids
		factor = order.factor
		labor_factor = order.labor_factor
#		print "startttttttttttt...................time", time.strftime('%M %S')
		sale_line = self.pool.get('sale.order.line')
		res_user = self.pool.get('res.users')
		#Adding code for Doc auth
		if order.doctype == 'doc':
			try:
				doc_title = order.document
				if not len(doc_title) > 0:
					raise osv.except_osv(_('User Error!'), _('Please give google spreadsheet title.'))
				username = res_user.browse(cr, uid, uid, context=context).gmail_user
				passwd = res_user.browse(cr, uid, uid, context=context).gmail_password
				import gdata.spreadsheet.service
				gd_client = gdata.spreadsheet.service.SpreadsheetsService()
				gd_client.email = username
				gd_client.password =passwd
				gd_client.ProgrammaticLogin()
				q = gdata.spreadsheet.service.DocumentQuery()
				q['title'] = doc_title
				q['title-exact'] = 'true'
				feed = gd_client.GetSpreadsheetsFeed(query=q)
				spreadsheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
				feed = gd_client.GetWorksheetsFeed(spreadsheet_id)
				worksheet_id = feed.entry[0].id.text.rsplit('/',1)[1]
				rows = gd_client.GetListFeed(spreadsheet_id, worksheet_id).entry
				row = rows[43]
				row2 = rows[44]
				row_key = row.custom.keys()[2]
				factor =row.custom[row_key].text
				row2_key = row2.custom.keys()[1]
				labor_factor = row2.custom[row2_key].text
			except Exception, e:
				raise osv.except_osv(_('User Error!'), _('Authenticate with Google Spreadsheet Fail Please see Configuration in Setting/User/Syncronization.'))       

		for line in order.order_line:
			sale_price = float(factor) * float(line.product_id.standard_price)
			labor_cost = float(labor_factor) * float(line.labor_cost)
			cr.execute("update sale_order_line set purchase_price=%s, labor_cost=%s where id=%s",[sale_price, labor_cost, line.id])
#			line.write({'purchase_price': sale_price,'labor_cost':labor_cost})
#		print "End----------------------------time", time.strftime('%M %S')
		order.write({'calculated' : False})
		return True

sale_order()

	
