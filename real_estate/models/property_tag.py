from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'property tag'
    name = fields.Char(string='name', required=True)

    property_ids = fields.Many2many('estate.property', string='tag')
