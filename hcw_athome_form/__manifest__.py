# Copyright 2014-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "HCW@Home - request consultation form (queues)",
    "summary": "Consultation request with HCW@Home through Queues",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Iabsis SARL",
    "maintainers": ["obitwo"],
    "website": "https://iabsis.com",
    "category": "",
    "depends": [
        "calendar",
        "website",
        "portal",
        "base",
        "hcw_athome"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/website.xml",
        'data/cron.xml',
    ],
    "demo": [],
    "installable": True,
    "images": ['static/description/main_screenshot.png']
}
