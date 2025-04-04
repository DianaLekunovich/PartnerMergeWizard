from odoo import http
from odoo.http import request
from odoo import sql_db

class PartnerController(http.Controller):
    @http.route('/partner/find_similar', type='json', auth='user')
    def find_similar_contacts(self, partner_id):
        partner = request.env['res.partner'].browse(partner_id)
        cr = sql_db.db_connect(request.cr.dbname).cursor()
        query = """
            SELECT id FROM res_partner
            WHERE (email = %s OR phone = %s) AND id != %s
        """
        cr.execute(query, (partner.email, partner.phone, partner.id))
        similar_ids = [row[0] for row in cr.fetchall()]
        cr.close()
        return similar_ids
