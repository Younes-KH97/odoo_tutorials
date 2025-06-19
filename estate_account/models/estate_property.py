from odoo import models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def set_sold(self):
        res = super().set_sold()

        if not self.buyer_id:
            raise UserError("Cannot create invoice without a buyer.")

        commission = self.selling_price * 0.06
        admin_fee = 100.00

        self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {
                    'name': f"Commission - {self.name}",
                    'quantity': 1,
                    'price_unit': commission,
                }),
                (0, 0, {
                    'name': "Administrative Fees",
                    'quantity': 1,
                    'price_unit': admin_fee,
                }),
            ],
        })

        return res