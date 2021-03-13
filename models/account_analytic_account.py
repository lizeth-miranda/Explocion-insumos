# -*- coding: utf-8 -*-
# instruccion para hacer importaciones desde odoo
from odoo import api, fields, models, exceptions, _
from odoo.exceptions import ValidationError, UserError


class acanac(models.Model):
    _inherit = 'account.analytic.account'

    limite_acero = fields.Monetary(
        string="Limite Acero",
    )
    limite_consu = fields.Monetary(
        string="Limite Consumible",
    )
