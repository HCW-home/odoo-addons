# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models
import random
import string

_logger = logging.getLogger(__name__)


class Users(models.Model):

    _inherit = 'res.users'
    _sql_constraints = [
        ('field_unique',
         'unique(secnum)',
         'Choose another value - it has to be unique!')
    ]

    def _random_sec_number(self):
        for user in self:
            user.secnum = ''.join(random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))

    secnum = fields.Char(
        string="Random security number", compute=_random_sec_number, store=True, index=True, required=True,
    )
