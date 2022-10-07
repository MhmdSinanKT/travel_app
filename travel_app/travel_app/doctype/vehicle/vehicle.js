// Copyright (c) 2022, Muhammed Sinan K T and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle', {
	refresh: function(frm) {
    if(!frm.is_new()){
      frm.add_custom_button('Reset Seat Booking', () => {
        let no_of_rows = frm.doc.seats.length
        frm.clear_table('booking_receipts')
        frm.refresh();
        frm.call('reset_seat_status', {no_of_rows: no_of_rows})
      })
    }
  }
});
