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
    hsfeURL = fields.Char(string="URL HsFE Services")
    hsUser = fields.Char(string="User HsFE Services")
    hsPassword = fields.Char(string="Password HsFE Services")
