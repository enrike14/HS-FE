# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class AccountMoveReversal(models.TransientModel):
	_inherit = "account.move.reversal"

	def _prepare_default_reversal(self, move):
		reversal = super(AccountMoveReversal, self)._prepare_default_reversal(move)
		reversal["reversal_reason_fe"] = self.reason or ""
		return reversal