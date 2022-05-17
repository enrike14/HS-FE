# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime
import logging

class customers_fields(models.Model):
	#_inherit = "product.product"
	#_name = "res.partner"
	_inherit = "res.partner"
	#asignar campos al modulo de res.partner
	@api.depends('name')
	def _get_country_id(self):
		country = self.pool.get('res.country')
		country_id = self.env['res.country'].search([['name', '=', 'Panama']]).id
		self.country_id = country_id

	TipoClienteFE = fields.Selection(
	[('01', 'Contribuyente'),
	('02', 'Consumidor final'),
	('03', 'Gobierno'),
	('04', 'Extranjero')],string = 'Tipo Cliente')
	tipoContribuyente = fields.Selection(
	[('1', 'Natural'),
	('2', 'Jurídico')],string = 'Tipo Contribuyente')
	numeroRUC =fields.Char(string="Número RUC",size=20)
	digitoVerificadorRUC=fields.Char(string="Digito Verificador RUC",size=2)
	razonSocial=fields.Char(string="Razón Social",size=100)
	direccion=fields.Char(string="Dirección",size=100)
	#ubicacion change
	#neonety_country_id = fields.Many2one('res.country', string='País', default=lambda self: self._get_country_id())
	country_id = fields.Many2one('res.country', string='País', default=lambda self: self._get_country_id())
	province_id = fields.Many2one('electronic.invoice.province', string='Provincia')
	district_id = fields.Many2one('electronic.invoice.district', string='Distrito')
	sector_id = fields.Many2one('electronic.invoice.sector', string='Corregimiento')
	#codigo
	CodigoUbicacion=fields.Char(string="Codigo Ubicación",size=8)
	provincia=fields.Char(string="Provincia",related='province_id.code')
	distrito=fields.Char(string="Distrito",related='district_id.code')
	corregimiento=fields.Char(string="Corregimiento",related='sector_id.code')
	tipoIdentificacion=fields.Selection(
	[('04', 'Extranjero'),
	('01', 'Pasaporte'),
	('02', 'Numero Tributario'),
	('99', 'Otro')],string = 'Tipo Identificación')
	nroIdentificacionExtranjero=fields.Char(string="Nro. de Pasaporte o Nro. de Identificación Tributaria Extranjera")
	paisExtranjero=fields.Char(string="País Extranjero",size=50)
	#telefono1	 ///correoElectronico1
	pais=fields.Char(string="País")
	paisOtro=fields.Char(string="País Otro",size=50)

	@api.onchange('TipoClienteFE')
	def on_change_tipoIdent(self):
		if str(self.TipoClienteFE)=='01' or str(self.TipoClienteFE)=='03':
			self.tipoContribuyente='2'
		elif str(self.TipoClienteFE)=='02' or str(self.TipoClienteFE)=='04':
			self.tipoContribuyente='1'
		else:
			self.tipoContribuyente=''
	
	def _get_country_id(self):
		self._cr.execute("SELECT id FROM res_country WHERE code LIKE 'PA' LIMIT 1")
		country_id = self._cr.fetchone()
		return country_id
	
	@api.onchange('province_id')
	def onchange_province_id(self):
		res = {}
		# self.district_id=""
		# self.sector_id=""

		if self.province_id:
			self._cr.execute('SELECT electronic_invoice_district.id, electronic_invoice_district.name FROM electronic_invoice_district WHERE electronic_invoice_district.province_id = %s AND electronic_invoice_district.country_id = ( SELECT electronic_invoice_province.country_id FROM electronic_invoice_province WHERE electronic_invoice_province.id = %s) ', (self.province_id.id, self.province_id.id))
			districts = self._cr.fetchall()
			ids = []

			for district in districts:
				ids.append(district[0])
			res['domain'] = {'district_id': [('id', 'in', ids)]}
		self.CodigoUbicacion=str(str(self.provincia)+"-"+str(self.distrito)+"-"+str(self.corregimiento))
		return res

	@api.onchange('district_id')
	def onchange_district_id(self):
		res = {}
		# self.sector_id=""
		if self.district_id:
			self._cr.execute('SELECT electronic_invoice_sector.id, electronic_invoice_sector.name FROM electronic_invoice_sector WHERE electronic_invoice_sector.district_id = %s AND  electronic_invoice_sector.country_id = ( SELECT electronic_invoice_district.country_id FROM electronic_invoice_district WHERE electronic_invoice_district.id = %s) ', (self.district_id.id, self.district_id.id))
			sectors = self._cr.fetchall()
			ids = []

			for sector in sectors:
				ids.append(sector[0])
			res['domain'] = {'sector_id': [('id', 'in', ids)]}
		self.CodigoUbicacion=str(str(self.provincia)+"-"+str(self.distrito)+"-"+str(self.corregimiento))
		return res
	
	@api.onchange('sector_id')
	def onchange_sector_id(self):
		self.CodigoUbicacion=str(str(self.provincia)+"-"+str(self.distrito)+"-"+str(self.corregimiento))
		