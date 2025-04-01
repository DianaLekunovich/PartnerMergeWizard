from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PartnerMergeWizard(models.TransientModel):
    _name = 'partner.merge.wizard'
    _description = 'Merge Partners Wizard'

    partner_ids = fields.Many2many('res.partner', string='Partners to Merge', required=True)
    main_partner_id = fields.Many2one('res.partner', string='Main Partner', required=True, domain="[('id', 'in', partner_ids)]")

    @api.model
    def default_get(self, fields):
        res = super(PartnerMergeWizard, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        if active_ids:
            partners = self.env['res.partner'].browse(active_ids)
            res['partner_ids'] = [(6, 0, partners.ids)]
        return res

    @api.constrains('partner_ids')
    def _check_partner_ids(self):
        for record in self:
            if len(record.partner_ids) < 2:
                raise UserError(_("You must select at least two partners to merge."))

    def action_merge(self):
        self.ensure_one()
        if not self.main_partner_id:
            raise UserError(_("You must select a main partner."))

        partner_ids_to_merge = self.partner_ids.ids
        partner_ids_to_merge.remove(self.main_partner_id.id)

        for partner_id in partner_ids_to_merge:

            sale_orders = self.env['sale.order'].search([('partner_id', '=', partner_id)])
            sale_orders.write({'partner_id': self.main_partner_id.id})

        unique_emails = list(set(self.partner_ids.mapped("email")))
        if len(unique_emails) > 1:
            return {
                'name': _('Choose Email'),
                'type': 'ir.actions.act_window',
                'res_model': 'partner.merge.email.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_partner_merge_wizard_id': self.id,
                            'partner_ids_to_archive': partner_ids_to_merge}
            }
        else:
            for partner_id in partner_ids_to_merge:
                self.env['res.partner'].browse(partner_id).write({'active': False})
            return {'type': 'ir.actions.act_window_close'}

class PartnerMergeEmailWizard(models.TransientModel):
    _name = 'partner.merge.email.wizard'
    _description = 'Choose Email for Merged Partner'

    partner_merge_wizard_id = fields.Many2one(
        'partner.merge.wizard',
        string="Merge Wizard",
        required=True
    )
    email_line_ids = fields.One2many(
        'partner.merge.email.line',
        'wizard_id',
        string="Emails"
    )

    @api.model
    def default_get(self, fields):
        res = super(PartnerMergeEmailWizard, self).default_get(fields)
        merge_wizard = self.env['partner.merge.wizard'].browse(self._context.get('default_partner_merge_wizard_id'))

        if merge_wizard.exists():
            emails = list(set(merge_wizard.partner_ids.mapped("email")))
            email_lines = [(0, 0, {'email': email}) for email in emails if email]
            res['email_line_ids'] = email_lines
        return res

    @api.constrains('email_line_ids')
    def _check_only_one_email_selected(self):
        for wizard in self:
            selected_emails = wizard.email_line_ids.filtered(lambda line: line.selected)
            if len(selected_emails) != 1:
                raise UserError(_("You must select exactly one email to continue."))

    def action_confirm_email(self):
        selected_email = self.email_line_ids.filtered(lambda e: e.selected)
        if self.partner_merge_wizard_id and selected_email:
            self.partner_merge_wizard_id.main_partner_id.write({'email': selected_email.email})
        for partner_id in self._context.get('partner_ids_to_archive'):
            self.env['res.partner'].browse(partner_id).write({'active': False})
        return {'type': 'ir.actions.act_window_close'}

class PartnerMergeEmailLine(models.TransientModel):
    _name = 'partner.merge.email.line'
    _description = 'Email Selection Line'

    wizard_id = fields.Many2one(
        'partner.merge.email.wizard',
        string="Wizard",
        required=True,
        ondelete='cascade'
    )
    email = fields.Char(string="Email", required=True)
    selected = fields.Boolean(string="Use this email")

