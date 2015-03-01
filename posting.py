# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
import logging
import meli_oerp_config


class mercadolibre_posting(osv.osv):
	_name = "mercadolibre.posting"
	_description = "Posting en MercadoLibre"
    
	_columns = {
		'posting_date': fields.date('Fecha del posting'), 
		'name': fields.char('Name'),
        	'meli_id': fields.char('Id del item asignado por Meli', size=256),
		'product_id': fields.many2one('product.product','product_id'),
        	'meli_status': fields.related( 'product_id','meli_status',relation='product.product',store=True,\
			string="Estado del producto en MLA",type='char' ),
	        'meli_permalink': fields.related( 'product_id','meli_permalink',relation='product.product',store=True,\
			 string="Permalink en MercadoLibre",type='char' ),
	        'meli_price': fields.related( 'product_id','meli_price',relation='product.product',store=True,\
			 string="Precio en MercadoLibre",type='float' ),
		}

mercadolibre_posting()

