// Copyright (c) 2022, Muhammed Sinan K T and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Booking', {

  setup:function(frm){
    frm.set_df_property('seats', 'read_only', 1)
  },

  on_submit: function(frm){
    frm.refresh();
    frm.call('get_seat_status')
  },

  refresh: function(frm){
    frm.clear_table('seats')
    if(frm.doc.type_of_vehicle == 'Public'){
      frm.add_custom_button('Refersh Seat Availability', () => {
        frm.clear_table('seats');
        frm.refresh();
        frm.call('get_seat_status')
      })
    }
  },

  type_of_vehicle: function(frm){
    frm.set_value('booking_cost', '')
  },

  starting_location: function(frm){
    if(frm.doc.starting_location == frm.doc.destination){
      frappe.msgprint('Starting Location and Destination cannot be the same')
      frm.set_value('starting_location','Select')
    }
    frm.set_value('vehicle','')
    frm.set_value('vehicle_name','')
    frm.set_value('driver_name','')
    frm.set_value('booking_cost','')
    frm.refresh();
  }

})
