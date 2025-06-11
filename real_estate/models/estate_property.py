from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

from odoo import api

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    name = fields.Char(string='Title', required=True)
    property_type_id = fields.Many2one("property.type", string="Type")
    salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('property.tag', string='tag')
    offer_ids = fields.One2many('property.offer', 'estate_property_id', string='offer')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From',
                                    default=lambda self: date.today() + relativedelta(months=3),
                                    copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Has Garage')
    garden = fields.Boolean(string='Has Garden', default=False)
    garden_area = fields.Integer(string='Garden Area (sqm)')
    
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string='Garden Orientation'
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        required=True,
        copy=False,
        default='new'
    )

    total_area = fields.Integer('total_area', compute="_compute_total")
    best_offer = fields.Float('best_offer', compute='_compute_best_offer')


    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # For mapped based method, see: https://github.com/odoo/odoo/blob/f011c9aacf3a3010c436d4e4f408cd9ae265de1b/addons/account/models/account_payment.py#L686
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(offer.price for offer in record.offer_ids)
            else:
                record.best_offer = 0.0  # or False or None, depending on your field type

    @api.onchange('garden')
    def _onchange_garden(self):
        message = None
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = ''
            message = "Click on 'Discard' to restore the previous garden values."
        else:
            self.garden_area = 10
            self.garden_orientation = 'north'
            message = "Click on 'Discard' to restore the original garden settings."
        # replace this warning instructions by other alert message
        if message:
            return {
                'warning': {
                    'title': "Information",
                    'message': message,
                }
            }
    
    def set_sold(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold")
        self.state = 'sold'

    def set_cancelled(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled")
        self.state = 'cancelled'