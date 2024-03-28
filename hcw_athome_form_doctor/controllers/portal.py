# Copyright 2024 Iabsis - Olivier Bitsch

import logging
from odoo.http import request, route
from odoo import http
import werkzeug
from odoo.exceptions import ValidationError, UserError

from odoo.addons.portal.controllers.portal import CustomerPortal
from hcw_py_sdk import HCW
_logger = logging.getLogger(__name__)


class AnonymousConsultationForm(http.Controller):

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

    @route("/invite/<string:secnum>", type="http", auth="public", website=True)
    def consultation_request(self, secnum):

        domain = [
            ('secnum', '=', secnum)
        ]
        user = request.env['res.users'].sudo().search(
            domain)

        if not len(user):
            return request.render("hcw_athome_form_doctor.invalid_request")

        patient_url = request.env['ir.config_parameter'].sudo().get_param(
            'hcw_athome.hcw_patient_url', default="")

        data = {
            'user': user,
            'invite': secnum,
            'patient_url': patient_url
        }

        return request.render("hcw_athome_form_doctor.consultation_request", data)

    @route("/consultation/create/<secnum>", type="http", auth="public", website=True, methods=['POST'])
    def consultation_create(self, secnum, **post):

        domain = [
            ('secnum', '=', secnum)
        ]
        user = request.env['res.users'].sudo().search(
            domain)

        if not len(user):
            return request.render("hcw_athome_form_doctor.invalid_request")

        invite_info = {
            "emailAddress": post['email'],
            "phoneNumber": post['phone'],
            "firstName": post['firstname'],
            "lastName": post['lastname'],
            "gender":  post['gender'],
            "patientTZ": http.request.env.user.tz,
            "sendInvite": False,
            "isPatientInvite": True,
            "doctorEmail": user.email
        }

        try:
            invite = self.hcw.invite.create(**invite_info)
        except Exception as e:
            _logger.exception(e)
            return request.render("hcw_athome_form_doctor.invalid_request")

        url = invite['invite']['patientURL']
        return werkzeug.utils.redirect(url, 303)


class CustomerPortalConsultation(CustomerPortal):

    def _prepare_portal_layout_values(self):
        d = super()._prepare_portal_layout_values()
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        if not 'localhost' in base_url:
            base_url = base_url.replace('http://', 'https://')
        d['base_url'] = base_url
        return d
