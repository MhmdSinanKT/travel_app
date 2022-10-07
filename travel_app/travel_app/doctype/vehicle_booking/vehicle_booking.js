// Copyright (c) 2022, Muhammed Sinan K T and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Booking', {

  on_submit:function(frm) {
    console.log('test');
    frm.clear_table('seats');
    frm.refresh();
    frm.call('alternate_get_seat_status_and_time')
  },

  refresh: function(frm) {
    frm.set_df_property('seats', 'read_only', 1)
    //Adds a button to update seat availability
    if(frm.doc.type_of_vehicle == 'Public'){
      frm.add_custom_button('Refersh Seat Availability', () => {
        frm.clear_table('seats');
        frm.refresh();
        frm.call('alternate_get_seat_status_and_time')
      })
    }
  },

	type_of_vehicle: function(frm) {
    if(frm.doc.type_of_vehicle == 'Public' ){
      frm.set_value('booking_cost','')
    }
    else {
      frm.set_value('vehicle','')
      frm.set_value('vehicle_name','')
      frm.set_value('driver_name','')
      frm.set_value('booking_cost','')
      frm.clear_table('passengers')
      frm.clear_table('seats');
      frm.refresh();
      frm.set_query('private_vehicle', () => {
        return {
          filters: {
            type: frm.doc.type_of_vehicle
          }
        }
      })
      frm.call('get_booking_cost').then(r => {
        let cost = r.message
        frm.set_value('booking_cost', cost)
      })
    }
	},

  starting_location: function(frm) {
    if(frm.doc.starting_location == frm.doc.destination){
      frappe.msgprint('Starting Location and Destination cannot be the same')
      frm.set_value('starting_location','Select')
    }
    frm.set_value('vehicle','')
    frm.set_value('vehicle_name','')
    frm.set_value('driver_name','')
    frm.set_value('booking_cost','')
    frm.set_value('starting_location_time','')
    frm.set_value('destination_time','')
    frm.clear_table('seats')
    if(frm.doc.destination != 'Select'){
      frm.call('get_vehicle_list').then(r => {
        let vehicles = r.message
        frm.set_value('vehicle', '')
        frm.set_df_property('vehicle', 'options', vehicles)
      })
    }
  },

  destination: function(frm) {
    if(frm.doc.starting_location == frm.doc.destination){
      frappe.msgprint('Starting Location and Destination cannot be the same')
      frm.set_value('destination','Select')
    }
    frm.set_value('vehicle','')
    frm.set_value('vehicle_name','')
    frm.set_value('driver_name','')
    frm.set_value('booking_cost','')
    frm.set_value('starting_location_time','')
    frm.set_value('destination_time','')
    frm.clear_table('seats')
    if(frm.doc.starting_location != 'Select'){
      frm.call('get_vehicle_list').then(r => {
        let vehicles = r.message
        frm.set_value('vehicle', '')
        frm.set_df_property('vehicle', 'options', vehicles)
      })
    }
  },

  vehicle: function(frm) {
    frm.clear_table('seats');
    frm.refresh();
    if(frm.doc.vehicle != '' && frm.doc.destination != 'Select' && frm.doc.starting_location != 'Select' && frm.doc.destination != frm.doc.starting_location){
      // frm.call('alternate_get_seat_status_and_time')
      frm.call('get_booking_cost').then(r => {
        let cost = r.message
        let no_of_passengers = frm.doc.passengers.length
        frm.set_value('booking_cost', cost * no_of_passengers)
        frm.call('alternate_get_seat_status_and_time')
      })
    }
  },

  date:function(frm) {
    if (frm.doc.vehicle != '' && frm.doc.destination != 'Select' && frm.doc.starting_location != 'Select' && frm.doc.destination != frm.doc.starting_location) {
      frm.clear_table('seats')
      frm.refresh();
      frm.call('alternate_get_seat_status_and_time')
    }
    let today = new Date().toISOString().slice(0, 10)
    let today_print_format = new Date().toLocaleDateString()
    if( today > frm.doc.date ){
      frappe.msgprint('Date cannot be before ' + today_print_format)
      frm.set_value('date',today)
    }
  }

});

frappe.ui.form.on('Passenger Table', {

  passengers_add: function(frm,cdt,cdn) {
    if(frm.doc.vehicle != '' && frm.doc.destination != 'Select' && frm.doc.starting_location != 'Select' && frm.doc.destination != frm.doc.starting_location){
      frm.call('get_booking_cost').then(r => {
        let cost = r.message
        let no_of_passengers = frm.doc.passengers.length
        frm.set_value('booking_cost', cost * no_of_passengers)
      })
    }
  },

  passengers_remove: function(frm,cdt,cdn) {
    if(frm.doc.route != 'Select'){
      frm.call('get_booking_cost').then(r => {
        let cost = r.message
        let no_of_passengers = frm.doc.passengers.length
        frm.set_value('booking_cost', cost * no_of_passengers)
      })
    }
  }

})
