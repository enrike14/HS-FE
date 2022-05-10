from odoo import models, fields, api

class FeCountry(models.Model):
	_name = 'res.country'
	_inherit = 'res.country'

	province_ids = fields.One2many('fe.province', 'country_id', string='Provincias', ondelete='cascade')