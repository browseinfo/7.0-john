from openerp.osv import fields, osv
from openerp.tools.translate import _
import xlrd

class sale_extends(osv.osv):
	_name = 'sale.extends'
	_description = "Sales Extend" 
	_columns = {
		'code' : fields.char('Code', size=64, required=False, readonly=False),
		'task_desc' : fields.char('Description', size=64, required=False, readonly=False),
		'prod_qty' : fields.float('Qty'),
		'uom_id':fields.many2one('product.uom', 'UOM', required=True),
	}
sale_extends()

class product_product(osv.osv):
	_inherit = 'product.product'
	_columns = {
		'time_factor': fields.float('Labour Factor'),
	}
product_product()


class sale_order(osv.osv):
    _inherit = 'sale.order'
    _columns = {
    'factor': fields.float('Factor'),
    'labor_factor': fields.float('Labor Factor'),
    'doctype':fields.selection([('factor','Factor'),('doc','Document Title')],'State', select=True, readonly=False),
    'document':fields.char('Document Title', size=64, required=False, readonly=False),
	'squre_meter': fields.float('Squre Meter'),
    'distance': fields.float('Distance'),
    'type':fields.char('Type', size=64),
    }
    _defaults = {
    	'doctype': 'factor',
    }
sale_order()


class sale_order_lines(osv.osv):
    _inherit = 'sale.order.line'
    _columns = {
    	'time_factor': fields.float('Labor Factor'),
        'labor_cost': fields.float('Labor Cost'),
		'extend_ids':fields.many2many('sale.extends', 'sale_extend_rel2', 'order_id','code', 'Project Detail '),
	}


    def button_calculate(self, cr, uid, ids, context={}):
        lines = self.pool.get('sale.order.line').browse(cr, uid, ids)
        cost_price = 0.0
        labor_cost = 0.0
        factor = 0.0
        labor_factor = 0.0
        res_user = self.pool.get('res.users')
        for line in lines:
        		if line.order_id.doctype == 'factor':
        			select_type = 'factor'
        			factor = line.order_id.factor
        			labor_factor = line.order_id.labor_factor
        			if not factor > 0.0:
        				raise osv.except_osv(_('User Error!'), _('Please Insert Factor Value.'))        
    			else:
    				select_type = 'doc'
    				doc_title = line.order_id.document
    				if not len(doc_title) > 0:
						raise osv.except_osv(_('User Error!'), _('Please give google spreadsheet title.'))    					 
        		cost_price = line.product_id.standard_price
        		time_factor = line.product_id.time_factor
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
					line.write({'price_unit': sale_price,'labor_cost':labor_cost})
				except Exception, e:
					raise osv.except_osv(_('User Error!'), _('Authenticate with Google Spreadsheet Fail Please see Configuration in Setting/User/Syncronization.'))        	

			else:
				sale_price = factor * cost_price
				labor_cost = labor_factor * time_factor
				line.write({'price_unit': sale_price,'labor_cost':labor_cost})
        return True

sale_order_lines()

	
