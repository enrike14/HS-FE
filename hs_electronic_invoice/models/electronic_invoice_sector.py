from odoo import models, fields, api
class electronic_invoice_sector(models.Model):
	_name = 'electronic.invoice.sector'
	code = fields.Char(string='Código', size=3, required=True)
	name = fields.Char(string='Nombre', size=255, required=True, translate=True)
	country_id = fields.Many2one('res.country', string='País', required=False, compute='_get_country_id', store=True)
	province_id = fields.Many2one('electronic.invoice.province', string='Provincia', required=False)
	district_id = fields.Many2one('electronic.invoice.district', string='Distrito', required=False)

	@api.depends('name')
	def _get_country_id(self):
		country = self.pool.get('res.country')
		country_id = self.env['res.country'].search([['name', '=', 'Panama']]).id
		self.country_id = country_id