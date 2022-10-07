# Copyright (c) 2022, Muhammed Sinan K T and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Vehicle(Document):

	@frappe.whitelist()
	def reset_seat_status(self, no_of_rows):
		#resets the seat booking status of seats of a vehicle
		for i in range(no_of_rows):
			if self.seats[i].c1 == 'Booked':
				self.seats[i].c1 = 'Available'
			if self.seats[i].c2 == 'Booked':
				self.seats[i].c2 = 'Available'
			if self.seats[i].c3 == 'Booked':
				self.seats[i].c3 = 'Available'
			if self.seats[i].c4 == 'Booked':
				self.seats[i].c4 = 'Available'
		self.save()
