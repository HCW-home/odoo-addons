from odoo import api, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    hcw_root_url = fields.Char(
        string="HCW@Home API URL",
        config_parameter='hcw_athome.hcw_api_url'
    )

    hcw_doctor_url = fields.Char(
        string="HCW@Home Doctor URL",
        config_parameter='hcw_athome.hcw_doctor_url'
    )

    hcw_patient_url = fields.Char(
        string="HCW@Home Patient URL",
        config_parameter='hcw_athome.hcw_patient_url'
    )

    hcw_scheduler_login = fields.Char(
        string="HCW@Home Scheduler login",
        config_parameter='hcw_athome.hcw_scheduler_login'
    )
    hcw_scheduler_pass = fields.Char(
        string="HCW@Home Scheduler password",
        config_parameter='hcw_athome.hcw_scheduler_pass'
    )

    hcw_shared_jwt = fields.Char(
        string="HCW@Home Shared JWT",
        config_parameter='hcw_athome.hcw_shared_jwt'
    )
