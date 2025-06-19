from odoo import models, fields

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 
                                   'salesperson', 
                                   string='property_ids',
                                   domain=[('state','in',('new','offer_received'))])