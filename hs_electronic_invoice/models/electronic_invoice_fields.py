# -*- coding: utf-8 -*-

import base64
from cmath import log
from io import BytesIO
from pydoc import cli
from odoo import models, fields, api
import zeep
import logging
from base64 import b64decode
from datetime import datetime, timezone
from odoo import http
from odoo.http import request
from odoo.http import content_disposition
import qrcode
from odoo.exceptions import UserError
import requests
import time
import json
from odoo.http import request
from odoo import http

_logger = logging.getLogger(__name__)


class electronic_invoice_fields(models.Model):
    _inherit = "account.move"
    lastFiscalNumber = fields.Char(
        string="Número Fiscal", compute="on_change_state", readonly="True", store="True")
    puntoFactFiscal = fields.Char(
        string="Punto Facturación Fiscal", readonly="True", default='')
    pagadoCompleto = fields.Char(
        string="Estado de Pago", compute="on_change_pago", readonly="True", store="True")
    qr_code = fields.Binary("QR Factura Electrónica",
                            attachment=True, readonly="True")
    tipo_documento_fe = fields.Selection(
        string='Tipo de Documento',
        readonly="True",
        selection=[
            ('01', 'Factura de operación interna'),
            ('02', 'Factura de importación'),
            ('03', 'Factura de exportación'),
            ('04', 'Nota de Crédito referente a una FE'),
            ('05', 'Nota de Débito referente a una FE'),
            ('06', 'Nota de Crédito genérica'),
            ('07', 'Nota de Débito genérica'),
            ('08', 'Factura de Zona Franca'),
            ('09', 'Reembolso'),
        ],
        default='01',
        help='Tipo de Documento para Factura Eletrónica.'
    )
    tipo_emision_fe = fields.Selection(
        string='Tipo de Emisión',
        readonly="True",
        selection=[
            ('01', 'Autorización de Uso Previa, operación normal'),
            ('02', 'Autorización de Uso Previa, operación en contingencia'),
            ('03', 'Autorización de Uso Posterior, operación normal'),
            ('04', ' Autorización de Uso posterior, operación en contingencia')
        ],
        default='01',
        help='Tipo de Emisión para Factura Eletrónica.'
    )
    fecha_inicio_contingencia = fields.Date(
        string='Fecha Inicio de Contingencia')
    motivo_contingencia = fields.Char(string='Motivo de Contingencia')
    naturaleza_operacion_fe = fields.Selection(
        string='Naturaleza de Operación',
        selection=[
            ('01', 'Venta'),
            ('02', 'Exportación'),
            ('10', 'Transferencia'),
            ('11', 'Devolución'),
            ('12', 'Consignación'),
            ('13', 'Remesa'),
            ('14', 'Entrega gratuita'),
            ('20', 'Compra'),
            ('21', 'Importación'),
        ],
        default='01',
        help='Naturaleza de Operación para Factura Eletrónica.'
    )
    tipo_operacion_fe = fields.Selection(
        string='Tipo de Operación',
        selection=[
            ('1', 'Salida o venta'),
            ('2', 'Entrada o compra (factura de compra- para comercio informal. Ej.: taxista, trabajadores manuales)'),
        ],
        default='1',
        help='Tipo de Operación para Factura Eletrónica.'
    )
    destino_operacion_fe = fields.Selection(
        string='Destino de Operación',
        selection=[
            ('1', 'Panamá'),
            ('2', 'Extranjero'),
        ],
        default='1',
        help='Destino de Operación para Factura Eletrónica.'
    )
    formatoCAFE_fe = fields.Selection(
        string='Formato CAFE',
        selection=[
            ('1', 'Sin generación de CAFE: El emisor podrá decidir generar CAFE en cualquier momento posterior a la autorización de uso de FE'),
            ('2', 'Cinta de papel'),
            ('3', 'Papel formato carta.'),
        ],
        default='1',
        help='Formato CAFE Factura Eletrónica.'
    )
    entregaCAFE_fe = fields.Selection(
        string='Entrega CAFE',
        selection=[
            ('1', 'Sin generación de CAFE: El emisor podrá decidir generar CAFE en cualquier momento posterior a la autorización de uso de FE'),
            ('2', 'CAFE entregado para el receptor en papel'),
            ('3', 'CAFE enviado para el receptor en formato electrónico'),
        ],
        default='1',
        help='Entrega CAFE Factura Eletrónica.'
    )
    envioContenedor_fe = fields.Selection(
        string='Envío de Contenedor',
        selection=[
            ('1', 'Normal'),
            ('2', ' El receptor exceptúa al emisor de la obligatoriedad de envío del contenedor. El emisor podrá decidir entregar el contenedor, por cualquier razón, en momento posterior a la autorización de uso, pero no era esta su intención en el momento de la emisión de la FE.'),
        ],
        default='1',
        help='Envío de Contenedor Eletrónica.'
    )
    procesoGeneracion_fe = fields.Selection(
        string='Proceso de Generación',
        selection=[
            ('1', 'Generación por el sistema de facturación del contribuyente (desarrollo propio o producto adquirido)'),
        ],
        default='1',
        readonly=True,
        help='Proceso de Generación de Factura Eletrónica.'
    )
    tipoVenta_fe = fields.Selection(
        string='Tipo de Venta',
        selection=[
            ('1', 'Venta de Giro del negocio'),
            ('2', 'Venta Activo Fijo'),
            ('3', 'Venta de Bienes Raíces'),
            ('4', 'Prestación de Servicio. Si no es venta, no informar este campo'),
        ],
        default='1',
        help='Tipo de venta Factura Eletrónica.'
    )
    tipoSucursal_fe = fields.Selection(
        string='Tipo de Sucursal',
        selection=[
            ('1', 'Mayor cantidad de Operaciones venta al detal (retail)'),
            ('2', 'Mayor cantidad de Operaciones venta al por mayor')
        ],
        default='1',
        help='Tipo de sucursal Eletrónica.'
    )

    reversal_reason_fe = fields.Char(
        string='Reason', readonly="True", store="True", default='')
    anulado = fields.Char(string='Anulado', readonly="True",
                          store="True", default='')
    nota_credito = fields.Char(
        string='Nota de Crédito', readonly="True", compute="on_change_type", default='')
    total_precio_descuento = fields.Float(
        string="Precio Descuento", default=0.00, store="True")
    hsfeURLstr = fields.Char(
        string='HermecURL', readonly="True", store="True", default='')
    pdfNumber = fields.Char(string="PDF Fiscal Number",
                            store="True", default='')
    tipoDocPdf = fields.Char(
        string="PDF Tipo Documento", store="True", default='')
    tipoEmisionPdf = fields.Char(
        string="PDF Tipo Emisión", store="True", default='')
    api_token = fields.Char(string="ApiToken", store="True", default='')
    puntoFacturacion = fields.Char(
        string="Punto Fac", store="True", default='')

    @api.depends('qr_code')
    def on_change_pago(self):
        for record in self:
            if str(record.qr_code) != "False":
                record.pagadoCompleto = 'FECompletada'
            else:
                record.pagadoCompleto = 'Pendiente'

    @api.depends('state')
    def on_change_state(self):
        for record in self:
            if record.state == 'posted' and record.pagadoCompleto != "NumeroAsignado":
                record.pagadoCompleto = "NumeroAsignado"
                if record.lastFiscalNumber == False:

                    document = self.env["electronic.invoice"].search(
                        [('name', '=', 'ebi-pac')], limit=1)
                    if document:
                        self.hsfeURLstr = document.hsfeURL
                        fiscalN = (
                            str(document.numeroDocumentoFiscal).rjust(10, '0'))
                        self.puntoFacturacion = (
                            str(document.puntoFacturacionFiscal).rjust(3, '0'))

                        record.lastFiscalNumber = fiscalN
                        record.puntoFactFiscal = self.puntoFacturacion

                        document.numeroDocumentoFiscal = str(
                            int(document.numeroDocumentoFiscal)+1)

    @api.depends('move_type', 'partner_id')
    def on_change_type(self):
        if self.move_type:
            for record in self:
                if record.move_type == 'out_refund' and str(record.amount_residual) == "0.0":
                    record.tipo_documento_fe = "04"
                    record.nota_credito = "NotaCredito"
                else:
                    record.nota_credito = ""
                    if record.move_type == 'out_refund' and record.state == "draft" and record.reversed_entry_id.id != False:
                        original_invoice_id = self.env["account.move"].search(
                            [('id', '=', self.reversed_entry_id.id)], limit=1)
                        if original_invoice_id:
                            payment = original_invoice_id.amount_residual
                            inv_monto_total = original_invoice_id.amount_total
                            if payment != inv_monto_total:
                                record.tipo_documento_fe = "09"
                                record.nota_credito = "Reembolso"
                            else:
                                self.tipo_documento_fe = "04"
                                self.nota_credito = "NotaCredito"
                    else:
                        if record.move_type == 'out_refund' and record.state == "draft" and record.reversed_entry_id.id == False:
                            record.tipo_documento_fe = "06"
                            record.nota_credito = "NotaCredito"
        else:
            record.nota_credito = ""

    # HSFE HSServices Calls Security

    def get_connection(self):
        files = []
        headers = {}
        user = ""
        hsurl = ""
        password = ""
        # constultamos el objeto de nuestra configuración del servicio
        config_document_obj = self.env["electronic.invoice"].search(
            [('name', '=', 'ebi-pac')], limit=1)
        if config_document_obj:
            user = config_document_obj.hsUser
            password = config_document_obj.hsPassword
            hsurl = config_document_obj.hsfeURL

        url = hsurl + "api/token"
        payload = {'username': user,
                   'password': password}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)
        respuesta = json.loads(response.text)
        logging.info("RES" + str(respuesta))

        if("access_token" in respuesta):
            self.api_token = respuesta["access_token"]
            self.send_fiscal_doc()
        else:
            body = "HS Services <br> <b style='color:red;'>Error -- " + \
                ":</b> ("+str(respuesta['detail'])+")<br>"
            self.message_post(body=body)
            logging.info("ERROR: Connection Fail -- " +
                         str(respuesta["detail"]))

    def get_pdf_token(self):
        files = []
        headers = {}
        user = ""
        hsurl = ""
        password = ""
        # constultamos el objeto de nuestra configuración del servicio
        config_document_obj = self.env["electronic.invoice"].search(
            [('name', '=', 'ebi-pac')], limit=1)
        if config_document_obj:
            user = config_document_obj.hsUser
            password = config_document_obj.hsPassword
            hsurl = config_document_obj.hsfeURL

        url = hsurl + "api/token"
        payload = {'username': user,
                   'password': password}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)
        respuesta = json.loads(response.text)
        logging.info("RES" + str(respuesta))

        if("access_token" in respuesta):
            self.api_token = respuesta["access_token"]
            self.get_pdf_fe()
        else:
            body = "HS Services <br> <b style='color:red;'>Error -- " + \
                ":</b> ("+str(respuesta['detail'])+")<br>"
            self.message_post(body=body)
            logging.info("ERROR: Connection Fail -- " +
                         str(respuesta["detail"]))

    def send_fiscal_doc(self):
        url = self.hsfeURLstr + "api/send"
        original_invoice_values = {}
        retencion = {}
        original_invoice_id = self.env["account.move"].search(
            [('id', '=', self.reversed_entry_id.id)], limit=1)

        if original_invoice_id:
            original_invoice_values = {
                "lastFiscalNumber": original_invoice_id.lastFiscalNumber,
                "tipoDocumento": original_invoice_id.tipo_documento_fe,
                "tipoEmision": original_invoice_id.tipo_emision_fe
            }

        # constultamos el objeto de nuestra configuración del servicio
        config_document_obj = self.env["electronic.invoice"].search(
            [('name', '=', 'ebi-pac')], limit=1)
        if config_document_obj:
            tokenEmpresa = config_document_obj.tokenEmpresa
            tokenPassword = config_document_obj.tokenPassword
            codigoSucursal = config_document_obj.codigoSucursalEmisor
            url_wsdl = config_document_obj.wsdl
            self.puntoFacturacion = config_document_obj.puntoFacturacionFiscal

        precioDescuento = '0'
        for item in self.invoice_line_ids:
            if item.discount > 0:
                precioDescuento = str(
                    (float(item.price_unit) * float(item.discount)) / 100)
                self.total_precio_descuento += float(precioDescuento)
        logging.info("VALORES DE TAX:::" +
                     str(json.loads(self.tax_totals_json)))
        totalTaxes = json.loads(self.tax_totals_json)
        arrayTaxes = totalTaxes["groups_by_subtotal"]["Untaxed Amount"]
        logging.info("VALORES ARRAY DE TAXES:::" +
                     str(arrayTaxes))

        if(len(arrayTaxes) > 1):
            retencion = {
                'codigoRetencion': "2",
                'montoRetencion':  str('%.2f' % round((self.amount_total - self.amount_untaxed), 2))
            }

        all_values = json.dumps({
            "wsdl_url": url_wsdl,
            "tokenEmpresa": tokenEmpresa,
            "tokenPassword": tokenPassword,
            "codigoSucursalEmisor": codigoSucursal,
            "tipoSucursal": self.tipoSucursal_fe,
            "datosTransacion": self.get_transaction_data(),
            "listaItems": self.get_items_invoice_info(),
            "subTotales": self.get_sub_totals(),
            "listaFormaPago": self.get_array_payment_info(),
            "amount_residual": self.amount_residual,
            "original_invoice": original_invoice_values,
            "retencion": retencion,
            "descuentoBonificacion": {
                "descDescuento": "Descuentos aplicados a los productos",
                "montoDescuento": str('%.2f' % round(self.total_precio_descuento, 2))}
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }

        logging.info("VALUES SEND" + str(all_values))
        res = requests.request(
            "POST", url, headers=headers, data=all_values)

        respuesta = json.loads(res.text)
        logging.info("RES" + str(respuesta))

        if(int(respuesta["codigo"]) == 200):
            self.insert_data_to_electronic_invoice_moves(
                respuesta, self.name)
            self.pdfNumber = respuesta["numeroDocumentoFiscal"]
            self.tipoDocPdf = respuesta["tipoDocumento"]
            self.tipoEmisionPdf = respuesta["tipoEmision"]

            tipo_doc_text = respuesta['mensaje']

            if 'qr' in respuesta and 'cufe' in respuesta:
                tipo_doc_text = "Factura Electrónica Creada" + \
                    " :<br> <b>CUFE:</b> (<a target='_blank' href='" + \
                    respuesta['qr']+"'>"+str(respuesta['cufe'])+")</a><br>"
                if self.tipo_documento_fe == "04":
                    tipo_doc_text = "Nota de Crédito Creada" + \
                        " :<br> <b>CUFE:</b> (<a target='_blank' href='" + \
                        respuesta['qr']+"'>" + \
                        str(respuesta['cufe'])+")</a><br>"

            if self.tipo_documento_fe == "09":
                tipo_doc_text = "Reembolso Creado Correctamente."

            body = tipo_doc_text

            self.message_post(body=body)

            # add QR in invoice info
            if 'qr' in respuesta:
                self.generate_qr(respuesta)

            ##self.download_pdf(self.lastFiscalNumber, respuesta['pdf_document'])
            if respuesta['mensaje'] == "Proceso de Anulación ejecutado con éxito.":
                original_invoice_id.state = "cancel"
            self.pagadoCompleto = "FECompletada"
            # self.action_download_fe_pdf(self.lastFiscalNumber)
        else:
            self.insert_data_to_logs(respuesta, self.name)
            body = "Factura Electrónica No Generada:<br> <b style='color:red;'>Error " + \
                respuesta['codigo']+":</b> ("+respuesta['mensaje']+")<br>"
            self.message_post(body=body)

    def get_array_payment_info(self):
        url = self.hsfeURLstr + "api/listpayments"
        #logging.info("URL COMPLETO:" + str(url))
        payments_items = self.env["account.payment"].search(
            [('ref', '=', self.name)])
        payments = [item.amount for item in payments_items]
        totalTaxes = json.loads(self.tax_totals_json)
        arrayTaxes = totalTaxes["groups_by_subtotal"]["Untaxed Amount"]
        payment_values = json.dumps({
            "payments_items": payments,
            "monto_impuesto_completo": str(arrayTaxes[0]["tax_group_amount"]),
            "amount_untaxed": self.amount_untaxed,
            "total_discount_price": self.total_precio_descuento
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }

        response = requests.request(
            "POST", url, headers=headers, data=payment_values)
        #logging.info('Info AZURE PAGOS: ' + str(response.text))
        return json.loads(response.text)

    def get_transaction_data(self):
        url = self.hsfeURLstr + "api/transactiondata"
        cufe_fe_cn = ""
        last_invoice_number = ""

        original_invoice_id = self.env["account.move"].search(
            [('id', '=', self.reversed_entry_id.id)], limit=1)
        if original_invoice_id:
            last_invoice_number = original_invoice_id.name

        original_invoice_info = self.env["electronic.invoice.moves"].search(
            [('invoiceNumber', '=', last_invoice_number)], limit=1)
        if original_invoice_info:
            cufe_fe_cn = original_invoice_info.cufe

        fiscalReferenciados = {
            "fechaEmisionDocFiscalReferenciado": self.invoice_date.strftime("%Y-%m-%dT%H:%M:%S-05:00"),
            "cufeFEReferenciada": cufe_fe_cn,
        }

        transaction_values = json.dumps({
            "tipoEmision": self.tipo_emision_fe,
            "tipoDocumento": self.tipo_documento_fe,
            "numeroDocumentoFiscal": self.lastFiscalNumber,
            "puntoFacturacionFiscal": self.puntoFacturacion,
            "naturalezaOperacion": self.naturaleza_operacion_fe,
            "tipoOperacion": self.tipo_operacion_fe,
            "destinoOperacion": self.destino_operacion_fe,
            "formatoCAFE": self.formatoCAFE_fe,
            "entregaCAFE": self.entregaCAFE_fe,
            "envioContenedor": self.envioContenedor_fe,
            "procesoGeneracion": self.procesoGeneracion_fe,
            "tipoVenta": self.tipoVenta_fe,
            "informacionInteres": self.narration if self.narration else "",
            "fechaEmision": self.invoice_date.strftime("%Y-%m-%dT%H:%M:%S-05:00"),
            "cliente": self.get_client_info(),
            "fechaInicioContingencia": self.fecha_inicio_contingencia.strftime("%Y-%m-%dT%I:%M:%S-05:00") if self.fecha_inicio_contingencia else None,
            "motivoContingencia": "Motivo Contingencia: " + str(self.motivo_contingencia) if self.motivo_contingencia else "Motivo Contingencia: N/A",
            "listaDocsFiscalReferenciados": fiscalReferenciados
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }
        logging.info("Transactions Values HS HERMEC" + str(transaction_values))
        response = requests.request(
            "POST", url, headers=headers, data=transaction_values)
        logging.info('Info AZURE TRANSACTION DATA: ' + str(response.text))
        return json.loads(response.text)

    def get_client_info(self):
        url = self.hsfeURLstr + "api/client"
        client_values = json.dumps({
            "tipoClienteFE": self.partner_id.TipoClienteFE,
            "tipoContribuyente": self.partner_id.tipoContribuyente,
            "numeroRUC": self.partner_id.numeroRUC,
            "pais": self.partner_id.country_id.code,
            "correoElectronico1": self.partner_id.email,
            "digitoVerificadorRUC": self.partner_id.digitoVerificadorRUC,
            "razonSocial": self.partner_id.razonSocial,
            "direccion": self.partner_id.direccion,
            "codigoUbicacion": self.partner_id.CodigoUbicacion,
            "provincia": self.partner_id.provincia,
            "distrito": self.partner_id.distrito,
            "corregimiento": self.partner_id.corregimiento,
            "tipoIdentificacion": self.partner_id.tipoIdentificacion,
            "nroIdentificacionExtranjero": self.partner_id.nroIdentificacionExtranjero,
            "paisExtranjero": self.partner_id.paisExtranjero
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }
        logging.info("Cliente Enviado:" + str(client_values))
        response = requests.request(
            "POST", url, headers=headers, data=client_values)
        #logging.info("URL Odoo:" + str(request.httprequest.host_url))

        logging.info('Info AZURE CLIENTE: ' + str(response.text))
        return json.loads(response.text)

    def get_sub_totals(self):
        url = self.hsfeURLstr + "api/subtotals"
        payments_items = self.env["account.payment"].search(
            [('ref', '=', self.name)])
        payments = [item.amount for item in payments_items]
        totalTaxes = json.loads(self.tax_totals_json)
        arrayTaxes = totalTaxes["groups_by_subtotal"]["Untaxed Amount"]

        sub_total_values = json.dumps({
            "amount_untaxed": self.amount_untaxed,
            "amount_tax_completed": str(arrayTaxes[0]["tax_group_amount"]),
            "total_discount_price": self.total_precio_descuento,
            "items_qty": str(len(self.invoice_line_ids)),
            "payment_time": 1,
            "array_total_items_value": payments,
            "array_payment_form": self.get_array_payment_info()
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }
        logging.info("SUBTOTALES Values HS HERMEC" + str(sub_total_values))
        response = requests.request(
            "POST", url, headers=headers, data=sub_total_values)
        #logging.info('Info AZURE SUBTOTALES: ' + str(response.text))
        return json.loads(response.text)

    def generate_qr(self, res):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(res['qr'])
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image

    def download_pdf(self, fiscalNumber, document):
        b64 = str(document)
        b64_pdf = b64  # base64.b64encode(pdf[0])
        # save pdf as attachment
        name = fiscalNumber
        return self.env['ir.attachment'].create({
            'name': name + str(".pdf"),
            'type': 'binary',
            'datas': b64_pdf,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })

    def insert_data_to_electronic_invoice_moves(self, res, invoice_number):

        # Save the move info
        self.env['electronic.invoice.moves'].create({
            'cufe': res['cufe'] if 'cufe' in res else "",
            'qr': res['qr'] if 'qr' in res else "",
            'invoiceNumber': invoice_number,
            'fechaRDGI': res['fechaRecepcionDGI'] if 'fechaRecepcionDGI' in res else "",
            'numeroDocumentoFiscal':  self.lastFiscalNumber,
            'puntoFacturacionFiscal': self.puntoFactFiscal,
        })

    def insert_data_to_logs(self, res, invoice_number):

        self.env['electronic.invoice.logs'].create({
            'codigo': res['codigo'],
            'mensaje': res['mensaje'],
            'resultado': res['resultado'],
            'invoiceNumber': invoice_number
        })

    def get_items_invoice_info(self):
        url = self.hsfeURLstr + "api/items"
        itemLoad = []
        array_tax_item = []
        if self.invoice_line_ids:
            for item in self.invoice_line_ids:

                if item.tax_ids:
                    for tax_item in item.tax_ids:
                        if tax_item.amount_type == 'percent':
                            array_tax_item.append({
                                'amount_type':	tax_item.amount_type,
                                'amount': tax_item.amount
                            })
                        elif tax_item.amount_type == 'group':
                            array_children = []

                            for child_tax_item in tax_item.children_tax_ids:

                                array_children.append(
                                    {
                                        'child_name': str(child_tax_item.name),
                                        'child_amount': str(child_tax_item.amount)
                                    })
                            array_tax_item.append({
                                'amount_type':	tax_item.amount_type,
                                'amount': tax_item.amount,
                                'group_tax_children': array_children
                            })

                itemLoad.append({
                    'typeCustomers': str(self.partner_id.TipoClienteFE),
                    'categoriaProducto': str(item.product_id.categoryProduct) if item.product_id.categoryProduct else "",
                    'descripcion': str(item.product_id.name),
                    'codigo': str(item.product_id.default_code) if item.product_id.default_code else "",
                    'arrayTaxes': array_tax_item,
                    'cantidad': item.quantity,
                    'precioUnitario': item.price_unit,
                    'precioUnitarioDescuento': item.discount,
                    'codigoGTIN':  str(item.product_id.codigoGTIN) if item.product_id.codigoGTIN else "",
                    'cantGTINCom': item.product_id.cantGTINCom if item.product_id.cantGTINCom else "",
                    'codigoGTINInv': item.product_id.codigoGTINInv if item.product_id.cantGTINCom else "",
                    'cantGTINComInv': item.product_id.cantGTINComInv if item.product_id.cantGTINComInv else "",
                    'fechaFabricacion': str(item.product_id.fechaFabricacion).strftime("%Y-%m-%dT%H:%M:%S-05:00") if item.product_id.fechaFabricacion else datetime.today().strftime("%Y-%m-%dT%H:%M:%S-05:00"),
                    'fechaCaducidad': str(item.product_id.fechaCaducidad).strftime("%Y-%m-%dT%H:%M:%S-05:00") if item.product_id.fechaCaducidad else datetime.today().strftime("%Y-%m-%dT%H:%M:%S-05:00"),
                    'codigoCPBS': str(item.product_id.codigoCPBS),
                    'unidadMedidaCPBS': str(item.product_id.unidadMedidaCPBS),
                    'codigoCPBSAbrev': str(item.product_id.codigoCPBSAbrev),
                    'tasaISC': str(item.product_id.tasaISC),
                    'precioAcarreo': item.product_id.precioAcarreo if item.product_id.precioAcarreo else 0.00,
                    'precioSeguro': item.product_id.precioSeguro if item.product_id.precioSeguro else 0.00,
                    'infoItem': str(item.product_id.infoItem) if item.product_id.infoItem else "",
                    'tasaOTI': str(item.product_id.tasaOTI) if item.product_id.tasaOTI else "",
                    'valorTasa': item.product_id.valorTasa if item.product_id.valorTasa else 0.00,
                })
                #self.narration if self.narration else "",
            # logging.info("ITEMS ENVIADOS::::::" + str(itemLoad))......
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }
        dataJsonItem = {"list_items": itemLoad}
        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(dataJsonItem))
        return json.loads(response.text)

    def get_pdf_fe(self):
        self.pagadoCompleto = "Finalizado"
        # constultamos el objeto de nuestra configuración del servicio
        config_document_obj = self.env["electronic.invoice"].search(
            [('name', '=', 'ebi-pac')], limit=1)
        if config_document_obj:
            tokenEmpresa = config_document_obj.tokenEmpresa
            tokenPassword = config_document_obj.tokenPassword
            codigoSucursal = config_document_obj.codigoSucursalEmisor
            url_wsdl = config_document_obj.wsdl
            self. puntoFacturacion = config_document_obj.puntoFacturacionFiscal
        url = self.hsfeURLstr + "api/pdf"

        pdf_values = json.dumps({
            "wsdl_url": url_wsdl,
            "codigoSucursalEmisor": codigoSucursal,
            "tokenEmpresa": tokenEmpresa,
            "tokenPassword": tokenPassword,
            "tipoEmision": self.tipoEmisionPdf,
            "tipoDocumento": self.tipoDocPdf,
            "numeroDocumentoFiscal": self.pdfNumber,
            "puntoFacturacionFiscal": self.puntoFacturacion,

        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(self.api_token)
        }

        logging.info('Enviado PDF:: ' + str(pdf_values))

        correcto = False
        #logging.info("PD 64" + str(response))
        while correcto != True:
            response = requests.request(
                "POST", url, headers=headers, data=pdf_values)
            respuesta = json.loads(response.text)
            logging.info('Resultado PDF:: ' + str(response.text))
            if respuesta["codigo"] == "200":
                correcto = True
                self.download_pdf(self.pdfNumber, str(respuesta["documento"]))
