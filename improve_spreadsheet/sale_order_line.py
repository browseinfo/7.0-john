from openerp.osv import fields, osv
from openerp.tools.translate import _
import xlrd
import openerp.addons.decimal_precision as dp

class sale_order_lines(osv.osv):
    _inherit = 'sale.order.line'

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.purchase_price * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
        
    _columns = {
		'purchase_price': fields.float('Cost Price', digits=(16,2)),
		'calculate': fields.boolean('Calculate'),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
	}
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False, name='', partner_id=False,lang=False, update_tax=True, date_order=False, packaging=False,fiscal_position=False, flag=False,prod_image=False, context=None):
		context = context or {}
		product_uom_obj = self.pool.get('product.uom')
		partner_obj = self.pool.get('res.partner')
		product_obj = self.pool.get('product.product')
		warning = {}
		res = super(sale_order_lines, self).product_id_change(cr, uid, ids, pricelist, product, qty=qty,
		uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
		lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, context=context)
		frm_cur = self.pool.get('res.users').browse(cr, uid, uid).company_id.currency_id.id
		to_cur = self.pool.get('product.pricelist').browse(cr, uid, [pricelist])[0].currency_id.id
		if not product:
			return res
		purchase_price = self.pool.get('product.product').browse(cr, uid, product).standard_price
		price = self.pool.get('res.currency').compute(cr, uid, frm_cur, to_cur, purchase_price, round=False)
		res['value'].update({'purchase_price': price})
		product_obj = product_obj.browse(cr, uid, product, context=context)
		res['value']['labor_cost'] = product_obj.time_factor
		return res

sale_order_lines()
