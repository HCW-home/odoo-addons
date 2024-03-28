# Copyright 2014-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "HCW@Home base configuration",
    "summary": """
        HCW@Home - Open Source Teleconsultation integration - base configuration""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Iabsis SARL",
    "maintainers": ["Olivier Bitsch"],
    "website": "https://hcw-at-home.com",
    'depends': ['base', 'mail', 'uom'],
    "data": [
        "views/config.xml",
    ],
    "demo": [],
    "installable": True,
    'images': ['banner_thumbnail.png']
}
