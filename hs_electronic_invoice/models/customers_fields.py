# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class customers_fields(models.Model):
	#_inherit = "product.product"
	#_name = "res.partner"
	_inherit = "res.partner"
	#asignar campos al modulo de res.partner
	TipoClienteFE = fields.Selection(
	[('01', 'Contribuyente'),
	('02', 'Consumidor final'),
	('03', 'Gobierno'),
	('04', 'Extranjero')],string = 'Tipo Cliente FE')
	tipoContribuyente = fields.Selection(
	[('1', 'Natural'),
	('2', 'Jurídico')],string = 'Tipo Contribuyente')
	numeroRUC =fields.Char(string="Número RUC")
	digitoVerificadorRUC=fields.Char(string="digitoVerificadorRUC")
	razonSocial=fields.Char(string="Razón Social")
	direccion=fields.Char(string="Dirección")
	CodigoUbicacion=fields.Char(string="Codigo Ubicación")
	provincia=fields.Char(string="Provincia")
	distrito=fields.Char(string="Distrito")
	corregimiento=fields.Char(string="Corregimiento")
	tipoIdentificacion=fields.Selection(
	[('04', 'Extranjero'),
	('01', 'Pasaporte'),
	('02', 'Numero Tributario'),
	('99', 'Otro')],string = 'Tipo Identificación')
	nroIdentificacionExtranjero=fields.Char(string="Nro. Identificación Extranjero")
	paisExtranjero=fields.Char(string="País Extranjero")
	#telefono1	 ///correoElectronico1
	pais=fields.Char(string="País")
	paisOtro=fields.Char(string="País Otro")
		