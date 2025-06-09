from odoo import models, fields

class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Type'
    name = fields.Char(string='name', required=True)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='property')