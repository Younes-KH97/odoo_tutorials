from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta

class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'property offer'
    price = fields.Float('price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='status',
    copy=False)
    partner_id = fields.Many2one('res.partner', string='partner_id')
    estate_property_id = fields.Many2one('estate.property', string='property')