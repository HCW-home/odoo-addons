# Copyright 2021 Tecnativa - Jairo Llopis
# Copyright 2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request, route
from odoo import http
import werkzeug
from odoo.exceptions import ValidationError, UserError

from hcw_py_sdk import HCW


class CustomerPortal(http.Controller):

    def __init__(self):
        self._hcw = None

    @property
    def hcw(self):
        if not self._hcw:
            hcw_api_url = request.env['ir.config_parameter'].sudo().get_param(
                'hcw_athome.hcw_api_url', default='')
            hcw_scheduler_login = request.env['ir.config_parameter'].sudo().get_param(
                'hcw_athome.hcw_scheduler_login', default='')
            hcw_scheduler_pass = request.env['ir.config_parameter'].sudo().get_param(
                'hcw_athome.hcw_scheduler_pass', default='')
            self._hcw = HCW(hcw_api_url, hcw_scheduler_login,
                            hcw_scheduler_pass)
        return self._hcw

    @route("/consultation/request", type="http", auth="user", website=True)
    def consultation_form(self):
        """Form for consultation request."""

        data = {"queues": self.hcw.queue.list}
        return request.render("hcw_athome_form.consultation_request", data)

    @route("/consultation/submit", type="http", auth="user", website=True, methods=['POST'])
    def create_consultation(self, **post):

        queue_name = None
        for queue in self.hcw.queue.list:
            if queue['id'] == post['queue']:
                queue_name = queue['name']

        if not queue_name:
            raise UserError("Queue name is missing")

        invite_info = {
            "emailAddress": post['email'],
            "phoneNumber": post['phone'],
            "firstName": post['firstname'],
            "lastName": post['lastname'],
            "gender":  post['gender'],
            "patientTZ": http.request.env.user.tz,
            "sendInvite": False,
            "isPatientInvite": True,
            "queue": queue_name
        }

        invite = self.hcw.invite.create(**invite_info)
        url = invite['invite']['patientURL']
        user_id = http.request.env.user.id

        request.env['hcw.consultation'].sudo().create(
            {
                "hcw_id": invite['invite']['id'],
                "patient_firstname": post['firstname'],
                "patient_lastname": post['lastname'],
                "patient_phone": post['phone'],
                "patient_email": post['email'],
                "hcw_link": url,
                "user_id": user_id,
                "state": "requested"
            }
        )

        return werkzeug.utils.redirect(url, 303)

    @route("/consultation/resume", type="http", auth="user", website=True)
    def consultation_resume(self):
        """
        Resume consultation action.
        TODO: have a way to reset the session token
        """

        domain = [
            ('state', '!=', 'closed'),
            ('user_id', '=', http.request.env.user.id)
        ]

        consultation = request.env['hcw.consultation'].search(
            domain, limit=1)

        return werkzeug.utils.redirect(consultation.hcw_link, 303)

    @route("/my/consultations", type="http", auth="user", website=True)
    def my_consultations(self):
        domain = [
            ('user_id', '=', http.request.env.user.id)
        ]

        consultations = request.env['hcw.consultation'].search(
            domain, limit=50)

        data = {'consultations': consultations}
        return request.render("hcw_athome_form.my_consultations", data)
