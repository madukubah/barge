 # -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError, ValidationError
import odoo.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class Barge(models.Model):
	_name = "shipping.barge"

	name = fields.Char(string="Name", size=100 , required=True)
	capacity = fields.Float( string="Capacity (WMT)", required=True, default=0, digits=dp.get_precision('Barge') )
	# shipping_ids = fields.One2many("shipping.shipping", inverse_name="barge_id", string="Shippings", readonly=True)
	warehouse_id = fields.Many2one(
            'stock.warehouse', 'Warehouse',
			required=True,
            ondelete="restrict")
	location_id = fields.Many2one(
            'stock.location', 'Location',
			readonly=True,
			domain=[ ('usage','=',"internal")  ],
            ondelete="restrict")
	procurement_rule_id = fields.Many2one(
            'procurement.rule', 'Procurement Rule',
			readonly=True,
            ondelete="restrict")
	active = fields.Boolean(
        'Active', default=True,
        help="If unchecked, it will allow you to hide the rule without removing it.")

	@api.model
	def create(self, values):
		StockLocation = self.env['stock.location'].sudo()
		ProcurementRule = self.env['procurement.rule'].sudo()
		StockPickingType = self.env['stock.picking.type'].sudo()
		StockWarehouse = self.env['stock.warehouse'].sudo()

		warehouse = StockWarehouse.search([ ("id", '=', values["warehouse_id"] ) ])
		picking_type = StockPickingType.search([ ("code", '=', "outgoing" ), ("warehouse_id", '=', values["warehouse_id"] ) ])
		if not picking_type:
			raise UserError(_("Cannot Find Picking Type For Procurement Rule ") )

		values["location_id"] = StockLocation.create({
							"name" : values["name"],
							"usage" : "internal",
							"location_id" : warehouse.view_location_id.id ,
						}).id

		values["procurement_rule_id"] = ProcurementRule.create({
							"name" : values["name"] + "-> Customer",
							"action" : "move",
							"location_src_id" : values["location_id"] ,
							"warehouse_id" : values["warehouse_id"] ,
							# "location_id" : self.env['ir.property'].get_param('property_stock_customer', '').split(',') ,
							"picking_type_id" : picking_type.id ,
						}).id
		res = super(Barge, self ).create(values)
		return res
	
	@api.multi
	def unlink(self):
		for rec in self:
			if rec.location_id:
				rec.location_id.toggle_active()
			if rec.procurement_rule_id:
				rec.procurement_rule_id.toggle_active()
		
		return super(Barge, self ).unlink()
		

