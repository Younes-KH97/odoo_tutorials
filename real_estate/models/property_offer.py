from odoo import models, fields
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api

class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'property offer'
    partner_id = fields.Many2one('res.partner', string='partner_id')
    estate_property_id = fields.Many2one('estate.property', string='property')
    price = fields.Float('price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='status',
    copy=False)

    validity = fields.Integer('validity', default=7)
    date_deadline = fields.Date(
                string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date).days


