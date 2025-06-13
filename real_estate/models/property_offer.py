from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

from odoo.tools.float_utils import float_compare

class PropertyOffer(models.Model):
    _name = 'property.offer'
    _description = 'property offer'
    _order = 'price desc'
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

    def accept_offer(self):
        self.estate_property_id.selling_price = self.price
        self.estate_property_id.buyer_id = self.partner_id
        self.status = 'accepted'

    def refuse_offer(self):
        self.status = 'refused'

    @api.constrains('price')
    def check_price(self):
        for record in self:
            if float_compare(self.price, 
                             self.estate_property_id.expected_price * 90/100,
                             precision_rounding=0.1) == -1 :
                raise ValidationError('Offer price should be at least 90%% of the expected price')

    _sql_constraints = [
        ('check_price', 
         'CHECK(price > 0)', 
         'The offer price must be strictly positive.'),
    ]