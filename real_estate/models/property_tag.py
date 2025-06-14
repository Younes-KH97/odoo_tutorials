from odoo import models, fields

class PropertyTag(models.Model):
    _name = 'property.tag'
    _description = 'property tag'
    _order = 'name'
    name = fields.Char(string='name', required=True)

    property_ids = fields.Many2many('estate.property', string='tag')
    color = fields.Integer('color')
    _sql_constraints = [
        ("name_check", "UNIQUE(name)", "Error message"),
    ]