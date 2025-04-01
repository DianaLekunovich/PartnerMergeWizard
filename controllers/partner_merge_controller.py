from odoo import http
from odoo.http import request
import json

class PartnerMergeController(http.Controller):

    @http.route('/partner/merge', type='json', auth='user')
    def merge_partners(self, partner_ids, main_partner_id):
        try:
            partner_ids = [int(partner_id) for partner_id in partner_ids]
            main_partner_id = int(main_partner_id)
            wizard = request.env['partner.merge.wizard'].create({
                'partner_ids': [(6, 0, partner_ids)],
                'main_partner_id': main_partner_id
            })
            result = wizard.action_merge()
            if result.get('type') == "ir.actions.act_window":
                return result
            else:
                return {'success': True, 'message': 'Partners merged successfully.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
