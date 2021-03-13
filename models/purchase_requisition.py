# -*- coding: utf-8 -*-
# instruccion para hacer importaciones desde odoo
from odoo import api, fields, models, _
from odoo.exceptions import UserError

# PURCHASE_REQUISITION_STATES = [
#     ('check', 'Check'),
#     ('draft', 'Draft'),
#     ('ongoing', 'Ongoing'),
#     ('lock', 'Bloqueado'),
#     ('in_progress', 'Confirmed'),
#     ('open', 'Bid Selection'),
#     ('done', 'Closed'),
#     ('cancel', 'Cancelled')
# ]


class purreq(models.Model):
    _inherit = 'purchase.requisition'

    total_acero2 = fields.Monetary(
        string="Total Acero",
        compute='get_total_acero',
    )
    state = fields.Selection(selection_add=[(('lock', 'Bloqueado'))])
    state_blanket_order = fields.Selection(
        selection_add=[(('lock', 'Bloqueado'))], compute='_set_state')
    # state = fields.Selection(PURCHASE_REQUISITION_STATES,
    #                          'Status', tracking=True, required=True,
    #                          copy=False, default='check')
    # state_blanket_order = fields.Selection(
    #     PURCHASE_REQUISITION_STATES, compute='_set_state')

    @api.depends('state')
    def _set_state(self):
        for requisition in self:
            requisition.state_blanket_order = requisition.state

    def action_check(self):
        for requisition_line in self.line_ids:
            if requisition_line.total_acero > requisition_line.limite_acero:
                self.write({'state': 'lock'})
            if requisition_line.total_consu > requisition_line.limite_consu:
                self.write({'state': 'lock'})

    def action_in_progress(self):
        res = super(purreq, self).action_in_progress()
        for requisition_line in self.line_ids:
            if requisition_line.total_acero > requisition_line.limite_acero:
                raise UserError(
                    _('Estas excediendo el limite de Acero para el proyecto'))
            if requisition_line.total_consu > requisition_line.limite_consu:
                raise UserError(
                    _('Estas excediendo el limite de Consumibles para el proyecto'))

        self.ensure_one()
        if not all(obj.line_ids for obj in self):
            raise UserError(
                _("You cannot confirm agreement '%s' because there is no product line.") % self.name)
        if self.type_id.quantity_copy == 'none' and self.vendor_id:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(
                        _('You cannot confirm the blanket order without price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(
                        _('You cannot confirm the blanket order without quantity.'))
                requisition_line.create_supplier_info()
            self.write({'state': 'ongoing'})
        else:
            self.write({'state': 'in_progress'})
        # Set the sequence number regarding the requisition type
        if self.name == 'New':
            if self.is_quantity_copy != 'none':
                self.name = self.env['ir.sequence'].next_by_code(
                    'purchase.requisition.purchase.tender')
            else:
                self.name = self.env['ir.sequence'].next_by_code(
                    'purchase.requisition.blanket.order')
        return res

    def action_lock(self):
        # for rec in self:
        #     rec.state = "draft"
        self.write({'state': 'draft'})
    # def get_total_acero(self):
    #     self.total_acero = sum(line.price_unit for line in self.line_ids)
