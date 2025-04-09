from odoo import http, sql_db
from odoo.http import request


class PartnerController(http.Controller):
    @http.route("/partner/find_similar", type="json", auth="user")
    def find_similar_contacts(self, partner_id):
        partner = request.env["res.partner"].browse(partner_id)

        try:
            # Handle case where email or phone might be None
            email = partner.email or ""
            phone = partner.phone or ""

            with sql_db.db_connect(request.cr.dbname).cursor() as cr:
                query = """
                    SELECT id FROM res_partner
                    WHERE (email = %s OR phone = %s) AND id != %s
                    AND (email != '' OR phone != '')
                """
                params = (email, phone, partner.id)
                cr.execute(query, params)
                similar_ids = [row[0] for row in cr.fetchall()]
                return similar_ids
        except Exception as e:
            request.env["ir.logging"].sudo().create(
                {
                    "name": "Find Similar Partners",
                    "type": "server",
                    "level": "error",
                    "message": str(e),
                }
            )
            return []
