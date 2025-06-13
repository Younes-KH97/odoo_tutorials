from odoo import models, fields

class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Type'
    _order = 'name'
    name = fields.Char(string='name', required=True)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='properties')

    _sql_constraints = [
        ('unique_property_type_name',
         'UNIQUE(name)',
         'The property type name must be unique.'),
    ]