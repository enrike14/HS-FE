# -*- coding: utf-8 -*-

from dataclasses import field
from email.policy import default
from odoo import models, fields, api
from datetime import datetime


class electronic_invoice(models.Model):
	_name = "electronic.invoice"
	name = fields.Char(string="Nombre")
	wsdl = fields.Char(string="URL WSDL")
	descripcion = fields.Char(string="Descripción")
	tokenEmpresa = fields.Char(string="Token Empresa")
	tokenPassword = fields.Char(string="Token Password")
	codigoSucursalEmisor = fields.Char(string="Código Sucursal")
	numeroDocumentoFiscal = fields.Integer(string="No. Documento Fiscal")
	puntoFacturacionFiscal = fields.Char(string="Punto Facturación Fiscal")


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
