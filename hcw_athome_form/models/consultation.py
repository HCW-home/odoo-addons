# -*- coding: utf-8 -*-

import logging
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import api, fields, models
from odoo.exceptions import UserError
from hcw_py_sdk import HCW


_logger = logging.getLogger(__name__)


class Consultations(models.TransientModel):

    _name = 'hcw.consultation'

    hcw_id = fields.Char(
        string="Consultation ID", required=True
    )

    hcw_link = fields.Char(
        string="URL to reach the consultation", required=True)

    patient_firstname = fields.Char(
        string="Patient firstname", required=True)
    patient_lastname = fields.Char(
        string="Patient lastname", required=True)
    patient_phone = fields.Char(
        string="Patient phone", required=True)
    patient_email = fields.Char(
        string="Patient email", required=True)

    STATE = [
        ("requested", 'Requested'),  # Requested by patient
        ("waiting", 'Waiting'),  # Waiting on doctor
        ("ongoing", 'On going'),  # Consultation on going with doctor
        ("closed", 'Closed')  # Consultation closed
    ]

    state = fields.Selection(
        STATE, string='Days of the week', required=True)

    user_id = fields.Many2one("res.users", required=True)

    @property
    def hcw(self):
        hcw_api_url = request.env['ir.config_parameter'].sudo().get_param(
            'hcw_athome.hcw_api_url', default='')
        hcw_scheduler_login = request.env['ir.config_parameter'].sudo().get_param(
            'hcw_athome.hcw_scheduler_login', default='')
        hcw_scheduler_pass = request.env['ir.config_parameter'].sudo().get_param(
            'hcw_athome.hcw_scheduler_pass', default='')
        return HCW(hcw_api_url, hcw_scheduler_login,
                   hcw_scheduler_pass)

    def start_sync(self, ids=None):
        domain = [('state', '!=', 'closed')]
        filtered_ids = self.search(domain, limit=10000).ids
        if ids:
            ids = list(set(filtered_ids) & set(ids))
        else:
            ids = filtered_ids
        res = None
        try:
            res = self.browse(ids)._update_state()
        except Exception:
            _logger.exception("Failed processing SMS queue")
        return res

    @api.model
    def _update_state(self):
        for consultation in self:

            # Get the state of the invite
            try:
                invite_state = self.hcw.invite.get(
                    consultation.hcw_id).get('status')
            except:
                # This is a tricks get consultation is closed, API returns 404
                # TODO: have a proper way to get consultation state
                invite_state = 'ACCEPTED'

            if invite_state == 'SENT':
                consultation.state = 'requested'
            elif invite_state == 'ACCEPTED':
                hcw_consultation = self.hcw.invite.consultation(
                    consultation.hcw_id)

                if not hcw_consultation.get('acceptedBy'):
                    consultation.state = 'waiting'
                elif hcw_consultation.get('acceptedBy') and not hcw_consultation.get('inviteCreatedAt'):
                    # Another tricks to check if consultation is on going (not always working)
                    # TODO: have a proper way to get consultation state
                    consultation.state = 'ongoing'
                else:
                    consultation.state = 'closed'


class CustomerPortalConsultation(CustomerPortal):

    def _prepare_portal_layout_values(self):
        d = super()._prepare_portal_layout_values()
        consultations = request.env['hcw.consultation'].sudo().search(
            [("user_id", "=", request.env.user.id)])
        d['consultation_count'] = len(consultations)
        return d
