from odoo import models, fields, api

class electronic_invoice_country(models.Model):
	_name = 'res.country'
	_inherit = 'res.country'

	province_ids = fields.One2many('electronic.invoice.province', 'country_id', string='Provincias', ondelete='cascade')