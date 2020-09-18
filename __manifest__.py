# -*- coding: utf-8 -*-

{
    'name': 'Barge',
    'version': '1.0',
    'author': 'Technoindo.com',
    'category': 'Shipping Barge Management',
    'depends': [
        "stock",
        "procurement"
    ],
    'data': [
        'views/barge.xml',

        "data/barge_data.xml",

        "security/ir.model.access.csv",
    ],
    'qweb': [
        # 'static/src/xml/cashback_templates.xml',
    ],
    'demo': [
        # 'demo/sale_agent_demo.xml',
    ],
    "installable": True,
	"auto_instal": False,
	"application": False,
}
