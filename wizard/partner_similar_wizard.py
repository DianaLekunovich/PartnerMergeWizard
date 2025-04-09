from odoo import fields, models


class PartnerSimilarWizard(models.TransientModel):
    _name = "partner.similar.wizard"
    _description = "Similar Partners Wizard"

    partner_ids = fields.Many2many("res.partner", string="Similar Partners")
