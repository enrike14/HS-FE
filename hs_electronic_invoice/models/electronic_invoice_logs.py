# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class electronic_invoice_logs(models.Model):
	_name = "electronic.invoice.logs"
	codigo = fields.Char(string="Código", readonly = "True")
	resultado = fields.Char(string="Resultado", readonly = "True")
	invoiceNumber = fields.Char(string="No. Factura", readonly = "True")
	mensaje = fields.Char(string="Mensaje", readonly = "True")
	actualDate = fields.Datetime(string="Fecha", readonly = "True", default=lambda self: fields.datetime.now())
	cufe = fields.Char(string="CUFE", readonly = "True")
	qr = fields.Char(string="QR", readonly = "True")
	fechaRep = fields.Char(string="Fecha Recepción", readonly = "True")
	nroProtocoloAutorizacion = fields.Char(string="Protocolo de Atorización", readonly = "True")
	fechaLimite = fields.Char(string="Fecha Limite", readonly = "True")
