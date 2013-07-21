# -*- coding: utf-8 -*-
##############################################################################
#
#    Product extened field
#    Copyright (C) 2004-2010 BrowseInfo(<http://www.browseinfo.in>).
#    $autor:
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


from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time


class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'pharmaceuticalform': fields.char('Pharmaceutical Form', size=64),
        'concentration': fields.char('Concentration', size=64),
        'serial_number': fields.char('Serial Number', size=64),
        'expiration_date': fields.date('Expiration Date'),
    }
