# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class electronic_invoice_cpbs(models.Model):
	_name = "electronic.invoice.cpbs"
	segmentoID =  fields.Char(string="Segmento ID")
	segmento =  fields.Char(string="Segmento")
	familiaID =  fields.Char(string="Familia ID")
	familia =  fields.Char(string="Familia")
 