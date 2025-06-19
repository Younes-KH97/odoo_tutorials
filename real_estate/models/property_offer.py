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
    property_type_id = fields.Many2one('property.type', related='estate_property_id.property_type_id')
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
    is_sold = fields.Boolean(compute='_compute_is_sold', string='is_sold')
    is_offer_accepted = fields.Boolean(compute='_compute_is_offer_accepted', 
                                       string='is_offer_accepted',
                                       default=False)
    
    _sql_constraints = [
        ('check_price_contraint', 
         'CHECK(price < 1000)', 
         'The offer price must be strictly positive.'),
    ]

    @api.depends('status')
    def _compute_is_offer_accepted(self):
        for rec in self:
            rec.is_offer_accepted = rec.estate_property_id.state in ('offer_accepted','sold','cancelled') 
    
    @api.depends('status')
    def _compute_is_sold(self):
        for record in self:
            if record.status == 'accepted':
                record.is_sold = True
            else:
                record.is_sold = False

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
        self.estate_property_id.state = 'offer_accepted'
        self.status = 'accepted'

    def refuse_offer(self):
        self.status = 'refused'

    @api.constrains('price')
    def check_price(self):
        for record in self:
            if float_compare(record.price, 
                             record.estate_property_id.expected_price * 90/100,
                             precision_rounding=0.01) == -1 :
                raise ValidationError('Offer price should be at least 90%% of the expected price')
    
    @api.constrains('price')
    def check_price_positivity(self):
        for record in self:
            if float_compare(record.price, 
                             0,
                             precision_rounding=0.01) == -1 :
                raise ValidationError('Offer price should be positive')

    @api.model_create_multi
    def create(self, vals):
        property_id = vals[0]["estate_property_id"]
        property = self.env["estate.property"].browse(property_id)
        offer_price = vals[0]["price"]
        if any(offer.price > offer_price for offer in property.offer_ids):
            raise UserError("There is already an offer with a higher price.")
        property.state = 'offer_received'
        return super().create(vals)


    