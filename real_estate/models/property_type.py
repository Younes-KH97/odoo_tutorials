from odoo import models, fields, api

class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Type'
    _order = 'name'
    name = fields.Char(string='name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='properties')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('property.offer', 'property_type_id', string='offer_ids')
    offer_count = fields.Char(compute='_compute_offer_count', string='offer_count', store=False)
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    _sql_constraints = [
        ('unique_property_type_name',
         'UNIQUE(name)',
         'The property type name must be unique.'),
    ]