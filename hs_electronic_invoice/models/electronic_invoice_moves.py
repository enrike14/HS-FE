# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class electronic_invoice_moves(models.Model):
	_name = "electronic.invoice.moves"
	cufe = fields.Char(string="CUFE")
	qr =  fields.Text(string="QR Code")
	invoiceNumber =  fields.Char(string="Número de Factura")
	fechaRDGI =  fields.Char(string="Fecha Recepción DGI")
	numeroDocumentoFiscal =  fields.Char(string="No. Doc. Fiscal")
	puntoFacturacionFiscal =  fields.Char(string="Pto. Facturación Fiscal")


"""     def action_bank_reconciliation_change(self):
		action_id = self.env.ref(
			"hs_bank_reconciliation.action_bank_reconciliation_change_wizard"
		)
		return {
			"name": action_id.name,
			"type": action_id.type,
			"res_model": action_id.res_model,
			"view_id": action_id.view_id.id,
			"view_mode": action_id.view_mode,
			"target": "new",
		} """
