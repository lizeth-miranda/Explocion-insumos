# -*- coding: utf-8 -*-
# instruccion para hacer importaciones desde odoo
from odoo import api, fields, models


class acmoli(models.Model):
    _inherit = 'product.template'

    consumible = fields.Boolean(
        string="Consumible",
    )
