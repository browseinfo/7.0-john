from openerp.osv import fields, osv
from openerp.tools.translate import _
import xlrd
import time
import gdata.spreadsheet.service
import gspread

class calulate_line(osv.osv_memory):

	def calculate_order_lines(self, cr, uid, ids, context={}):
		active_ids = context.get('active_ids')
		lines = self.pool.get('sale.order.line').browse(cr, uid, active_ids)
		res_user = self.pool.get('res.users')
		for line in lines:
			cost_price = line.product_id.standard_price
			time_factor = line.product_id.time_factor
			if line.order_id.doctype == 'factor':
				select_type = 'factor'
				factor = line.order_id.factor
				labor_factor = line.order_id.labor_factor
				sale_price = factor * cost_price
				labor_cost = labor_factor * time_factor
				line.write({'purchase_price': sale_price,'labor_cost':labor_cost, 'calculate': True})
			else:
				select_type = 'doc'
				doc_title = line.order_id.document
				if not len(doc_title) > 0:
					raise osv.except_osv(_('User Error!'), _('Please give google spreadsheet title.'))
			if not select_type == 'factor':
				try:
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
					sale_price = float(factor) * float(cost_price)
					labor_cost = float(labor_factor) * float(time_factor)
					line.write({'purchase_price': sale_price,'labor_cost':labor_cost, 'calculate': True})
				except Exception, e:
					raise osv.except_osv(_('User Error!'), _('Authenticate with Google Spreadsheet Fail Please see Configuration in Setting/User/Syncronization.'))   			
		return True

	_name = 'calculate.line'
	_columns = {
		'name': fields.char('Name', size=64),
	}
calulate_line()
