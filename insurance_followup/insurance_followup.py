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

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time


class insurance_department(osv.osv):
    _description = "Insurance  Department"
    _name = 'insurance.department'
    _columns = {
                'name': fields.char('Name', size=64, required=True),
                'code': fields.char('Code', size=64 ),
    }

insurance_department()

class insurance_follwup(osv.osv):
    """ insurance_follwup """
    _name = "insurance.follwup"
    _description = "insurance follwup"
    _columns = {
        'name': fields.char('Name', size=64, required=True, states={'paid':[('readonly',True)]},),
        'surname': fields.char('Surname', size=64, states={'paid':[('readonly',True)]},),
        'address_id': fields.many2one('res.partner', 'Address', states={'paid':[('readonly',True)]},),
        'phone': fields.char('Phone', size=64, states={'paid':[('readonly',True)]},),
        'email': fields.char('Email', size=240, states={'paid':[('readonly',True)]},),
        'issue_date': fields.date('Issue Date', readonly=True, states={'draft':[('readonly',False)]}, select=True ),
        'date_due': fields.date('Payment Date', readonly=True, states={'draft':[('readonly',False)]}, select=True, required=True),
        'expiry_date': fields.date('CREDIT CARD EXPIRATION DATE', states={'paid':[('readonly',True)]},),
        'payment_frequency': fields.integer('FREQUENCY OF PAYMENT', states={'paid':[('readonly',True)]},),
        'sum_insured': fields.integer('SUM INSURED', states={'paid':[('readonly',True)]},),
        'no_of_policy': fields.integer('Number of Policy', states={'paid':[('readonly',True)]},),
        'company_id': fields.many2one('res.company', 'Company', states={'paid':[('readonly',True)]},),
        'prime': fields.char('Prime', size=64, states={'paid':[('readonly',True)]},),
        'form': fields.char('Form', size=64, states={'paid':[('readonly',True)]},),
        'plan': fields.char('Plan', size=64, states={'paid':[('readonly',True)]},),
        'user_id': fields.many2one('res.users', 'Agent', states={'paid':[('readonly',True)]},),
        'partner_id': fields.many2one('res.partner', 'Customer', states={'paid':[('readonly',True)]},),
        'department_id':fields.many2one('insurance.department', 'Insurance Department', states={'paid':[('readonly',True)]},),
        'amount': fields.float('Amount',required=True,),
        'state': fields.selection([
            ('draft','Draft'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
            ],'Status', select=True,),
        'notes': fields.text('Notes'),
        
    }
    _defaults ={
        'state' : 'draft'
    }    
insurance_follwup()
    
class insurance_follwup_followup(osv.osv):
    _name = 'insurance_follwup.followup'
    _description = 'Insurance Follow-up'
    _rec_name = 'name'
    _columns = {
        'followup_line': fields.one2many('insurance_follwup.followup.line', 'followup_id', 'Follow-up'),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'name': fields.related('company_id', 'name', string = "Name"),
    }
    _defaults = {
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'insurance_follwup.followup', context=c),
    }
    _sql_constraints = [('company_uniq', 'unique(company_id)', 'Only one follow-up per company is allowed')] 
    
insurance_follwup_followup()

class insurance_follwup_followup_line(osv.osv):
    _name = 'insurance_follwup.followup.line'
    _description = 'Follow-up Criteria'
    _columns = {
        'name': fields.char('Follow-Up Action', size=64, required=True),
        'sequence': fields.integer('Sequence', help="Gives the sequence order when displaying a list of follow-up lines."),
        'delay': fields.integer('Due Days', help="The number of days after the due date of the invoice to wait before sending the reminder.  Could be negative if you want to send a polite alert beforehand.", required=True),
        'followup_id': fields.many2one('insurance_follwup.followup', 'Follow Ups', required=True, ondelete="cascade"),
        'description': fields.text('Printed Message', translate=True),
        'send_email':fields.boolean('Send an Email', help="When processing, it will send an email"),
        'email_template_id':fields.many2one('email.template', 'Email Template', ondelete='set null'),
        'state': fields.selection([
            ('before','Before'),
            ('after','After'),
            ],'Status', select=True,required=True),
    }
    _order = 'sequence'
    _sql_constraints = [('days_uniq', 'unique(followup_id, delay)', 'Days of the follow-up levels must be different')]
    _defaults = {
        'send_email': True,
    }

insurance_follwup_followup_line()
