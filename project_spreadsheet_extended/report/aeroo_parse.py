from report import report_sxw
from datetime import datetime

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.total = 0.0
        self.time = 0.0
        self.no_page = 0
        self.localcontext.update({
            'get_total' : self.get_total,
            'main_total' : self.main_total,
            'get_date' : self.get_date,
            'get_time_factor':self.get_time_factor,
            'total_time_factor':self.total_time_factor,
            'get_sale_order':self.get_sale_order,
            'get_invoice' : self.get_invoice,
        })
        self.context = context

    def get_total(self,qty,price):
        self.total += qty*price
        return qty*price
    
    def main_total(self):
        tot = self.total
        self.total = 0.0
        return tot
    
    def get_date(self,date):
        a = datetime.strptime(date, '%Y-%m-%d')
        return a.strftime('%d/%m/%Y')
    
    def get_time_factor(self,time_factor1):
        self.time += time_factor1
        return time_factor1
    
    def total_time_factor(self):
        tf = self.time
        self.time=0.0
        return tf
    
    def get_sale_order(self,extend_id, order_id):
        sale_order_line_pool = self.pool.get('sale.order.line')
        sale_ids = sale_order_line_pool.search(self.cr,self.uid,[('extend_ids','in',extend_id),('order_id','=',order_id)])
        return sale_order_line_pool.browse(self.cr,self.uid,list(set(sale_ids)))
    
    def get_invoice(self, order_lines):
        extend_ids = []
        for line in order_lines:
            for extend in line.extend_ids:
                extend_ids.append(extend.id)
        extend_ids = list(set(extend_ids))
        a = self.pool.get('sale.extends').browse(self.cr, self.uid, extend_ids)
        print "A           ",a
        return a
