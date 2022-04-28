from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class product_field(models.Model):
	_inherit = "product.product"
	#_inherit = "product.template"
	#asignar campos al modulo de product.product
	categoryProduct = fields.Selection(
	[('Sin Categoría', 'Sin Categoría'),
	('Materia prima Farmacéutica', 'Materia prima Farmacéutica'),
	('Medicina', 'Medicina'),
	('Alimento', 'Alimento')],string = 'Categoría del Producto')
	fechaFabricacion = fields.Date(string='Fecha de Fabricación')
	fechaCaducidad = fields.Date(string='Fecha de Caducidad')
	codigoCPBSAbrev = fields.Char(string="CodigoCPBSAbrev")
	codigoCPBS = fields.Char(string="CodigoCPBS")
	unidadMedidaCPBS = fields.Char(string="UnidadMedidaCPBS")
	codigoGTIN = fields.Char(string="CodigoGTIN")
	codigoGTINInv = fields.Char(string="CodigoGTINInv")
	tasaISC = fields.Char(string="Tasa ISC")
	valorISC = fields.Char(string="Valor ISC")
	tasaOTI = fields.Char(string="Tasa OTI")
	valorTasa = fields.Char(string="Valor Tasa")
	