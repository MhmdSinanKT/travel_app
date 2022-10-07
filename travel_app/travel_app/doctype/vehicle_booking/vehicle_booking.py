# Copyright (c) 2022, Muhammed Sinan K T and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
import datetime

class VehicleBooking(Document):

	def validate(self):
		if self.type_of_vehicle == 'Select':
			frappe.throw('Select a Vehicle type to proceed')
		if self.type_of_vehicle == 'Public':
			if self.starting_location == 'Select':
				frappe.throw('Select a Starting Location to proceed')
			if self.destination == 'Select':
				frappe.throw('Select a Destination to proceed')
			if self.starting_location == self.destination:
				frappe.throw('Stating Location and Destination cannot be the same')
		if not self.vehicle:
			frappe.throw('Select a Vehicle to proceed')
		self.validate_seat()

	def before_submit(self):
		self.validate_payment()
		# self.book_seat()

	def on_submit(self):
		self.create_receipt()

	def on_cancel(self):
		self.cancel_seat_booking()

	def validate_seat(self):
		#checks if all the seats in the passenger table is available
		vehicle = frappe.get_doc('Vehicle',self.vehicle)
		for passenger in self.passengers:
			if passenger.seat_column == 'Select':
				frappe.throw('Select a Seat column for <b>{0}<b>'.format(passenger.name1))
			else:
				seat_col = passenger.seat_column
			if passenger.seat_row == 'Select':
				frappe.throw('Select a Seat row for <b>{0}<b>'.format(passenger.name1))
			else:
				seat_row = int(passenger.seat_row)-1
			if seat_col == 'C1':
				if vehicle.seats[seat_row].c1 == 'Booked':
					frappe.throw('Seat <b>C1-{0}</b> is already booked'.format(passenger.seat_row))
			elif seat_col == 'C2':
				if vehicle.seats[seat_row].c2 == 'Booked':
					frappe.throw('Seat <b>C2-{0}</b> is already booked'.format(passenger.seat_row))
			elif seat_col == 'C3':
				if vehicle.seats[seat_row].c3 == 'Booked':
					frappe.throw('Seat <b>C3-{0}</b> is already booked'.format(passenger.seat_row))
			elif seat_col == 'C4':
				if vehicle.seats[seat_row].c4 == 'Booked':
					frappe.throw('Seat <b>C4-{0}</b> is already booked'.format(passenger.seat_row))

	# def alternate_validate_seat(self):
	# 	vehicle = frappe.get_doc('Vehicle',self.vehicle)
	# 	for


	def validate_payment(self):
		#checks payment status
		if self.payment_status == 'Not Paid':
			frappe.throw('Complete the Payment to Proceed')

	def create_receipt(self):
		#makes receipts for each passenger and adds them to table in vehicle doctype
		vehicle = frappe.get_doc('Vehicle', self.vehicle)
		for passenger in self.passengers:
			vehicle.append('booking_receipts', {
				'booking_id': self.name,
				'vehicle_id': self.vehicle,
				'date': self.date,
				'passenger_name': passenger.name1,
				'contact_no': passenger.contact_no,
				'seat_column': passenger.seat_column,
				'seat_row': passenger.seat_row,
				'boarding_point': self.starting_location,
				'destination': self.destination
			})
		vehicle.save()

	# def book_seat(self):
	# 	#books the seats in the vehicle
	# 	vehicle = frappe.get_doc('Vehicle', self.vehicle)
	# 	for passenger in self.passengers:
	# 		seat_row = int(passenger.seat_row)-1
	# 		seat_col = passenger.seat_column
	# 		if seat_col == 'C1':
	# 			if vehicle.seats[seat_row].c1 == 'Available':
	# 				vehicle.seats[seat_row].c1 = 'Booked'
	# 		elif seat_col == 'C2':
	# 			if vehicle.seats[seat_row].c2 == 'Available':
	# 				vehicle.seats[seat_row].c2 = 'Booked'
	# 		elif seat_col == 'C3':
	# 			if vehicle.seats[seat_row].c3 == 'Available':
	# 				vehicle.seats[seat_row].c3 = 'Booked'
	# 		elif seat_col == 'C4':
	# 			if vehicle.seats[seat_row].c4 == 'Available':
	# 				vehicle.seats[seat_row].c4 = 'Booked'
	# 	vehicle.save()

	def cancel_seat_booking(self):
		#cancel the seats booked in the vehicle
		vehicle = frappe.get_doc('Vehicle', self.vehicle)
		# for passenger in self.passengers:
		# 	seat_row = int(passenger.seat_row)-1
		# 	seat_col = passenger.seat_column
		# 	if seat_col == 'C1':
		# 		if vehicle.seats[seat_row].c1 == 'Booked':
		# 			vehicle.seats[seat_row].c1 = 'Available'
		# 	elif seat_col == 'C2':
		# 		if vehicle.seats[seat_row].c2 == 'Booked':
		# 			vehicle.seats[seat_row].c2 = 'Available'
		# 	elif seat_col == 'C3':
		# 		if vehicle.seats[seat_row].c3 == 'Booked':
		# 			vehicle.seats[seat_row].c3 = 'Available'
		# 	elif seat_col == 'C4':
		# 		if vehicle.seats[seat_row].c4 == 'Booked':
		# 			vehicle.seats[seat_row].c4 = 'Available'
		frappe.db.delete('Booking Receipt', {
			'parent': vehicle.name,
			'booking_id': self.name
		})
		vehicle.save()

	@frappe.whitelist()
	def get_booking_cost(self):
		#gets cost of booking for a selected Vehicle
		settings = frappe.get_doc('Travel App Settings')
		if self.type_of_vehicle == 'Public':
			vehicle = frappe.get_doc('Vehicle', self.vehicle)
			for i in vehicle.stops:
				if i.stop == self.starting_location:
					starting_distance = i.distance
				elif i.stop == self.destination:
					destination_distance = i.distance
			distance = destination_distance - starting_distance
			distance -= 25
			if distance > 0:
				return 50 + (distance * 3)
			else:
				return 50
		elif self.type_of_vehicle == 'Private':
			return settings.advance_for_private_vehicle

	@frappe.whitelist()
	def get_seat_status_and_time(self):
		#gets the seat booking status of a vehicle at the time of function call
		vehicle = frappe.get_doc('Vehicle',self.vehicle)
		for i in vehicle.seats:
			self.append('seats', {
				'c1': i.c1,
				'c2': i.c2,
				'c3': i.c3,
				'c4': i.c4
			})
		#loop for getting the starting time of a vehicle and calculate the time of arrival at boarding point and destination of the passenger
		for j in vehicle.stops:
			if j.stop == self.starting_location:
				self.starting_location_time = ((vehicle.starting_time + datetime.datetime.strptime(j.time, '%H:%M:%S')).time())
			elif j.stop == self.destination:
				self.destination_time = ((vehicle.starting_time + datetime.datetime.strptime(j.time, '%H:%M:%S')).time())

	@frappe.whitelist()
	def alternate_get_seat_status_and_time(self):
		vehicle = frappe.get_doc('Vehicle', self.vehicle)
		for i in vehicle.seats:
			self.append('seats', {
				'c1': i.c1,
				'c2': i.c2,
				'c3': i.c3,
				'c4': i.c4
			})
		bflag = 0
		dflag = 0
		for stop in vehicle.stops:
			if bflag == 0 or dflag == 0:
				if stop.stop == self.starting_location and bflag == 0:
					user_boarding_idx = stop.idx
					bflag = 1
				elif stop.stop == self.destination and dflag == 0:
					user_destination_idx = stop.idx
					dflag = 1
		for receipt in vehicle.booking_receipts:
			boarding_point = receipt.boarding_point
			destination = receipt.destination
			date = receipt.date
			user_date = getdate(self.date)
			bflag = 0
			dflag = 0
			for stop in vehicle.stops:
				if bflag == 0 or dflag == 0:
					if stop.stop == boarding_point and bflag == 0:
						boarding_point_idx = stop.idx
						bflag = 1
					elif stop.stop == destination and dflag == 0:
						destination_idx = stop.idx
						dflag = 1
			if user_boarding_idx <= boarding_point_idx and user_destination_idx >= destination_idx and date == user_date:
				if receipt.seat_column == 'C1':
					self.seats[int(receipt.seat_row)-1].c1 = 'Booked'
				elif receipt.seat_column == 'C2':
					self.seats[int(receipt.seat_row)-1].c2 = 'Booked'
				elif receipt.seat_column == 'C3':
					self.seats[int(receipt.seat_row)-1].c3 = 'Booked'
				elif receipt.seat_column == 'C4':
					self.seats[int(receipt.seat_row)-1].c4 = 'Booked'
		#loop for getting the starting time of a vehicle and calculate the time of arrival at boarding point and destination of the passenger
		for j in vehicle.stops:
			if j.stop == self.starting_location:
				self.starting_location_time = ((vehicle.starting_time + datetime.datetime.strptime(j.time, '%H:%M:%S')).time())
			elif j.stop == self.destination:
				self.destination_time = ((vehicle.starting_time + datetime.datetime.strptime(j.time, '%H:%M:%S')).time())


	@frappe.whitelist()
	def get_vehicle_list(self):
		list = frappe.get_list('Route',
			filters = {
				'stop': self.starting_location
			},
			pluck = 'parent')
		vehicles = []
		for i in list:
			vehicle = frappe.get_doc('Vehicle',i)
			flag = 0
			for k in vehicle.stops:
				if k.stop == self.starting_location:
					starting_distance = k.distance
			for j in vehicle.stops:
				if j.stop == self.destination and j.distance > starting_distance:
					flag = 1
			if flag == 1:
				vehicles.append(vehicle.name)
		return vehicles
