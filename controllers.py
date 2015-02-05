from openerp import http
from bottle import template

import melisdk
from melisdk.meli import Meli

from openerp.osv import fields, osv
from openerp.http import request


from meli_oerp_config import *

class MercadoLibre(http.Controller):
    @http.route('/meli/', auth='public')
    def index(self):

        cr, uid, context = request.cr, request.uid, request.context
        company = request.registry.get('res.company').browse(cr,uid,1)
        CLIENT_ID = company.mercadolibre_client_id
        CLIENT_SECRET = company.mercadolibre_secret_key
        ACCESS_TOKEN = company.mercadolibre_access_token
        REFRESH_TOKEN = company.mercadolibre_refresh_token

        if (ACCESS_TOKEN==''):
            meli = Meli(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)
            return "<a href='"+meli.auth_url(redirect_URI=REDIRECT_URI)+"'>Login</a>"

        meli = Meli(client_id=CLIENT_ID,client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
        response = meli.get("/items/MLA533830652")

        return "MercadoLibre for Odoo 8 - Moldeo Interactive: %s " % response.content


class MercadoLibreLogin(http.Controller):

    @http.route(['/meli_login'], type='http', auth="user", methods=['GET'], website=True)
    def index(self, **codes ):
        cr, uid, context = request.cr, request.uid, request.context
        company = request.registry.get('res.company').browse(cr,uid,1)
        CLIENT_ID = company.mercadolibre_client_id
        CLIENT_SECRET = company.mercadolibre_secret_key

        meli = Meli(client_id=CLIENT_ID,client_secret=CLIENT_SECRET)

        codes.setdefault('code','none')
        codes.setdefault('error','none')
        codes.setdefault('error_description', 'none')
        if codes['error']!='none':
            message = "ERROR: %s" % codes['error']            
            message+= " DESCRIPTION: %s" % codes['error_description']
            return "<h1>"+message+"</h1><br/><a href='"+meli.auth_url(redirect_URI=REDIRECT_URI)+"'>Login</a>"

        if codes['code']!='none':
            print "Meli: Authorize: REDIRECT_URI: %s, code: %s" % ( REDIRECT_URI, codes['code'] )
            meli.authorize( codes['code'], REDIRECT_URI)
            ACCESS_TOKEN = meli.access_token
            REFRESH_TOKEN = meli.refresh_token
            company.write({'mercadolibre_access_token': ACCESS_TOKEN, 'mercadolibre_refresh_token': REFRESH_TOKEN, 'mercadolibre_code': codes['code'] } )
            return template('LOGGED WIT CODE: {{code}} <br>ACCESS_TOKEN: {{access_token}} <br>REFRESH_TOKEN: {{refresh_token}} <br>MercadoLibre for Odoo 8 - Moldeo Interactive <br><a href="javascript:window.history.go(-2);">Volver a Odoo</a> <script>window.history.go(-2)</script>', code=codes['code'], access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN )
        else:
            return "<a href='"+meli.auth_url(redirect_URI=REDIRECT_URI)+"'>Login</a>"

class MercadoLibreAuthorize(http.Controller):
    @http.route('/meli_authorize/', auth='public')
    def index(self):
        return "AUTHORIZE: MercadoLibre for Odoo 8 - Moldeo Interactive"


class MercadoLibreLogout(http.Controller):
    @http.route('/meli_logout/', auth='public')
    def index(self):
        return "LOGOUT: MercadoLibre for Odoo 8 - Moldeo Interactive"










