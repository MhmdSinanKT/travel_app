# Copyright (c) 2022, Muhammed Sinan K T and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class VehicleOwner(Document):
	#concatenates first and last names for the full name of the user
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'
