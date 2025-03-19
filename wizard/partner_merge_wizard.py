from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PartnerMergeWizard(models.TransientModel):
    _name = 'partner.merge.wizard'
    _description = 'Merge Partners Wizard'

    def _get_selection(self):
        selection=[("huih", "yugyugyg")]
        selection.append(("uj", self.main_partner_id.email))
        return selection

    partner_ids = fields.Many2many('res.partner', string='Partners to Merge', required=True)
    main_partner_id = fields.Many2one('res.partner', string='Main Partner', required=True, domain="[('id', 'in', partner_ids)]")

    email_choice = fields.Selection([
        ('main', 'Use main partner email'),
        ('other', 'Choose from duplicates'),
    ], default='main')
    email_options = fields.Selection(
        selection='_compute_email_options_selection',
        string='Choose email',
        readonly=False,
        #compute='_compute_email_options_selection',
        #inverse='_inverse_default_email'
    )

    @api.model
    def default_get(self, fields):
        res = super(PartnerMergeWizard, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        if active_ids:
            partners = self.env['res.partner'].browse(active_ids)
            res['partner_ids'] = [(6, 0, partners.ids)]
        print("get")
        return res

    @api.constrains('partner_ids')
    def _check_partner_ids(self):
        for record in self:
            if len(record.partner_ids) < 2:
                raise UserError(_("You must select at least two partners to merge."))

    def _get_email_options(self):
        """Returns the list of available email addresses"""
        options = []
        if self.email_choice == 'other' and self.partner_ids:
            print("get email func")
            for partner in self.partner_ids:
                if partner.email and partner.email not in [option[0] for option in options]:
                    options.append((partner.email, partner.email))
        return options

    #@api.depends('partner_ids', 'main_partner_id')
    @api.model
    def _compute_email_options_selection(self):
        """Dynamic selection options for email_options"""
        options = [("dianalekunovic@gmail.com","bkhkjnkn")]
        #print(self.partner_ids.ids)
        print(self.partner_ids.ids)
        if self.partner_ids.ids:
            for id in self.partner_ids.ids:
                email = self.env['res.partner'].browse(id).email
                if email:
                    options.append((email, email))

        """if self.main_partner_id.email and self.main_partner_id.email not in [option[0] for option in options]:
            options.insert(0, (self.main_partner_id.email, self.main_partner_id.email))"""
        #print(options)
        #self._fields['email_options'].selection = options
        return options

    @api.onchange('partner_ids', 'email_choice', 'main_partner_id')
    def _onchange_email_options(self):
        self._compute_email_options_selection()

    @api.depends('email_choice', 'partner_ids', 'main_partner_id')
    def _compute_email_options(self):
        if self.email_choice == 'main':
            self.email_options = self.main_partner_id.email if self.main_partner_id.email else False
        else:
            options = []
            for partner in self.partner_ids:
                if partner.email and partner.email not in [option[0] for option in options]:
                    options.append((partner.email, partner.email))
            self.email_options = options[0][0] if options else False

    def action_merge(self):
        self.ensure_one()
        if not self.main_partner_id:
            raise UserError(_("You must select a main partner."))

        partner_ids_to_merge = self.partner_ids.ids
        partner_ids_to_merge.remove(self.main_partner_id.id)

        for partner_id in partner_ids_to_merge:

            sale_orders = self.env['sale.order'].search([('partner_id', '=', partner_id)])
            sale_orders.write({'partner_id': self.main_partner_id.id})

            self.env['res.partner'].browse(partner_id).write({'active': False})

        return {'type': 'ir.actions.act_window_close'}
