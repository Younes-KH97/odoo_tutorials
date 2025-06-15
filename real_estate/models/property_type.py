from odoo import models, fields

class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Type'
    _order = 'name'
    name = fields.Char(string='name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    _sql_constraints = [
        ('unique_property_type_name',
         'UNIQUE(name)',
         'The property type name must be unique.'),
    ]