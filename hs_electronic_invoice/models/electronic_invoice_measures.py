# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class electronic_invoice_measures(models.Model):
	_name = "electronic.invoice.measures"
	name= fields.Char(string="Nombre",size=20)
	symbol= fields.Char(string="Simbolo")
	system=fields.Char(string="Sistema")
	measures=fields.Char(string="Medida")
	comments=fields.Char(string="Comentario")
	def name_get(self):
		result = []
		for record in self:
			record_name = record.symbol
			result.append((record.id, record_name))
		return result