from odoo import models, fields, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_sold(self):
        res = super().set_sold()  # call the original logic

        for property in self:
            if not property.buyer_id:
                raise UserError("Cannot create invoice without a buyer.")
            
            invoice = self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [(0, 0, {
                    'name': f"Property sold: {property.name}",
                    'quantity': 1,
                    'price_unit': property.selling_price,
                })],
            })

        return res
