from datetime import date

from sqlalchemy import select

from app.models import (
	Customer,
	Inventory,
	Mechanic,
	Service_Ticket,
	ServiceTicketInventory,
	db,
)


def seed_database():
	"""Insert the sample records used by the deployed application.

	Records are looked up by their existing unique or stable fields so this
	function can safely run every time the Render service starts.
	"""
	customers = {}
	for values in [
		{
			"name": "Amina Carter",
			"email": "amina.carter@example.com",
			"phone": "404-555-0101",
			"password": "Pyramid123!",
		},
		{
			"name": "Marcus Reed",
			"email": "marcus.reed@example.com",
			"phone": "404-555-0102",
			"password": "Pyramid123!",
		},
	]:
		customer = db.session.scalar(
			select(Customer).where(Customer.email == values["email"])
		)
		if customer is None:
			customer = Customer(**values)
			db.session.add(customer)
		customers[values["email"]] = customer

	mechanics = {}
	for values in [
		{
			"name": "Jordan Ellis",
			"email": "jordan.ellis@example.com",
			"phone": "404-555-0111",
			"salary": 68000.00,
		},
		{
			"name": "Riley Morgan",
			"email": "riley.morgan@example.com",
			"phone": "404-555-0112",
			"salary": 72000.00,
		},
	]:
		mechanic = db.session.scalar(
			select(Mechanic).where(Mechanic.email == values["email"])
		)
		if mechanic is None:
			mechanic = Mechanic(**values)
			db.session.add(mechanic)
		mechanics[values["email"]] = mechanic

	inventory = {}
	for values in [
		{"name": "Synthetic Motor Oil", "price": 39.99, "quantity": 25},
		{"name": "Oil Filter", "price": 12.50, "quantity": 40},
		{"name": "Brake Pad Set", "price": 89.99, "quantity": 15},
		{"name": "Air Filter", "price": 24.99, "quantity": 30},
	]:
		item = db.session.scalar(
			select(Inventory).where(Inventory.name == values["name"])
		)
		if item is None:
			item = Inventory(**values)
			db.session.add(item)
		inventory[values["name"]] = item

	db.session.flush()

	tickets = {}
	ticket_values = [
		{
			"customer": customers["amina.carter@example.com"],
			"service_date": date(2026, 9, 20),
			"description": "Routine oil change and air filter replacement",
			"vin": "1HGBH41JXMN109186",
			"mechanics": [mechanics["jordan.ellis@example.com"]],
			"parts": [("Synthetic Motor Oil", 1), ("Oil Filter", 1), ("Air Filter", 1)],
		},
		{
			"customer": customers["marcus.reed@example.com"],
			"service_date": date(2026, 9, 22),
			"description": "Front brake pad replacement",
			"vin": "1FTFW1ET5EFA12345",
			"mechanics": [mechanics["riley.morgan@example.com"]],
			"parts": [("Brake Pad Set", 1)],
		},
	]

	for values in ticket_values:
		ticket = db.session.scalar(
			select(Service_Ticket).where(Service_Ticket.vin == values["vin"])
		)
		if ticket is None:
			ticket = Service_Ticket(
				customer=values["customer"],
				service_date=values["service_date"],
				description=values["description"],
				vin=values["vin"],
			)
			db.session.add(ticket)
			db.session.flush()

		for mechanic in values["mechanics"]:
			if mechanic not in ticket.mechanics:
				ticket.mechanics.append(mechanic)

		for item_name, quantity in values["parts"]:
			item = inventory[item_name]
			association = db.session.scalar(
				select(ServiceTicketInventory).where(
					ServiceTicketInventory.service_ticket_id == ticket.id,
					ServiceTicketInventory.inventory_id == item.id,
				)
			)
			if association is None:
				ticket.inventory_associations.append(
					ServiceTicketInventory(inventory=item, quantity=quantity)
				)

		tickets[values["vin"]] = ticket

	db.session.commit()
	return tickets
