from odoo import http

class TestApi(http.Controller):

    @http.route('/api/v1/greeting', methods=["GET"], type='http', auth='none', csrf=False)
    def method_name(self , **kw):
        print("Saha world")

    
