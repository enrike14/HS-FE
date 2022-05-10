from odoo import models, fields, api
class FeDistrict(models.Model):
	_name = 'fe.district'

	code = fields.Char(string='Código', size=3, required=True, translate=True)
	name = fields.Char(string='Nombre', size=255, required=True, translate=True)
	country_id = fields.Many2one('res.country', string='País', required=False, translate=True, compute='_get_country_id', store=True)
	province_id = fields.Many2one('fe.province', string='Provincia', required=False, translate=True)
	#sector_ids = fields.One2many('fe.sector', 'district_id', string='Corregimientos')

	@api.depends('name')
	def _get_country_id(self):
		country = self.pool.get('res.country')
		country_id = self.env['res.country'].search([['name', '=', 'Panama']]).id
		self.country_id = country_id