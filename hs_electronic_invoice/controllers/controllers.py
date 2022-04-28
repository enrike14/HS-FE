# -*- coding: utf-8 -*-
from odoo import http

# class MyModule(http.Controller):
#     @http.route('/hs_module/hs_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hs_module/hs_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hs_module.listing', {
#             'root': '/hs_module/hs_module',
#             'objects': http.request.env['hs_module.hs_module'].search([]),
#         })

#     @http.route('/hs_module/hs_module/objects/<model("hs_module.hs_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hs_module.object', {
#             'object': obj
#         })