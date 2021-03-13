# -*- coding: utf-8 -*-
# instruccion para hacer importaciones desde odoo
from odoo import api, fields, models


class purreqlne(models.Model):
    _inherit = 'purchase.requisition.line'

    cate = fields.Char(
        related="product_id.categ_id.name",
        string="Categoria",
    )
    consumible = fields.Boolean(
        related="product_id.consumible",
    )
    total_acero = fields.Monetary(
        string="Total acero",
        compute="_total_acero",
    )
    total_consu = fields.Monetary(
        string="Total Consumible",
        compute="_total_consu",
    )
    currency_id = fields.Many2one(
        'account.analytic.account', 'currency',
    )
    limite_acero = fields.Monetary(
        related="account_analytic_id.limite_acero"
    )
    limite_consu = fields.Monetary(
        related="account_analytic_id.limite_consu"
    )

    @api.depends('price_unit')
    def _total_acero(self):
        for acero in self:
            acero.total_acero = sum(self.env['purchase.requisition.line'].search([
                ('cate', '=', acero.cate),
                ('cate', '=', 'ACERO'),
                ('account_analytic_id', '=', acero.account_analytic_id.name)
            ]).mapped('price_unit'))
            #acero.total_acero = acero.total_acero * -1

    @api.depends('price_unit')
    def _total_consu(self):
        for consu in self:
            consu.total_consu = sum(self.env['purchase.requisition.line'].search([
                #('cate', '!=', consu.cate),
                ('consumible', '=', True),
                ('account_analytic_id', '=', consu.account_analytic_id.name)
            ]).mapped('price_unit'))
