--Add Guest
INSERT INTO guest (reservation_id, f_name, l_name, area_code, phone_number) 
  VALUES (:reservation_id, :f_name_input, :l_name_input, :area_code_input, :phone_number_input);

--Update Guest
UPDATE guest 
  SET reservation_id = :reservation_id, f_name = :f_name_input,  l_name = :l_name_input, area_code= :area_code_input,  phone_number= :phone_number_input 
  WHERE id=:guest_Id_input;

--Delete Guest
DELETE FROM guest WHERE guest_id = :guest_Id_from_update_form;

--Read Entire Guest Table
SELECT * FROM guest;

--Add Room
INSERT INTO room (room_num, room_type, max_guests, price) 
  VALUES (:room_num_input, :room_type_input, :max_guests_input, price_input);

--Update Room
UPDATE room 
  SET room_type = :room_type_input, max_guests = :max_guests_input, price = :price_input 
  WHERE room_num = :room_num_input;

--Delete Room
DELETE FROM room WHERE room_num = :room_num_from_update_form;

--Read Entire Room Table
SELECT * FROM room;

--Add Reservation
INSERT INTO reservation (guest_id, payment_id, room_num, check_in, check_out, num_guests, confirmation_num)  
  VALUES (:guest_id, :payment_id, :room_num, :check_in_input, :check_out_input, :num_guests_input, :generated_confirmation_num);

--Update Reservation
UPDATE reservation 
  SET guest_id = :guest_id, payment_id = :payment_id, room_num = :room_num, check_in = :check_in_input, check_out = :check_out_input, num_guests = :num_guests_input, confirmation_num = :generated_confirmation_num 
  WHERE reservation_id = :reservation_id_from_update_form;

--Delete Reservation
DELETE FROM reservation WHERE reservation_id = :reservation_id_from_update_form;

--Read Entire Reservation Table
SELECT * FROM reservation;

--Add Payment
INSERT INTO payment (reservation_id, f_name, l_name, cc_num, cc_type, cc_security_code, house_num, street, city, state, zip_code, country, total_charged) 
  VALUES (:reservation_id, :f_name_input, :l_name_input, :cc_num_input, :cc_type_input, :cc_security_code_input, :house_num_input, :street_name_input, :city_input, :state_input, :zip_code_input, :country_input, :total_charged_from_reservation);

--Update Payment
UPDATE payment 
  SET reservation_id = :reservation_id, f_name = :f_name_input, l_name = :l_name_input, cc_num = :cc_num_input, cc_type = :cc_type_input, cc_security_code = :cc_security_code_input, house_num = :house_num_input, street = :street_name_input, city = :city_input, state =:state_input, zip_code = :zip_code_input, country = :country_input, total_charged = :total_charged_from_reservation 
  WHERE payment_id = :payment_id_from_update_form;

--Delete Payment
DELETE FROM payment WHERE payment_id = :payment_id_from_update_form;

--Read Entire Payment Table
SELECT * FROM payment; 

--Check availability button (list open rooms to make a reservation)
-- Find the rooms for the reservations made within that check in and out time
-- display rooms that are not those ones, and can hold the number of guests needed
SELECT * FROM room 
WHERE max_guests >= %s AND room_num NOT IN
( 
   SELECT DISTINCT room.room_num FROM room
   JOIN reservation_room ON room.room_num = reservation_room.room_num
   JOIN reservation ON reservation_room.reservation_id = reservation.reservation_id
   WHERE ((DATE %s < check_in and DATE %s >= check_in)
        or (DATE %s >= check_in and DATE %s <= check_out)));

--Read guest_room table
SELECT * FROM guest_room;

--Add guest_room
INSERT INTO guest_room (guest_id, room_num) VALUES (:guest_id, :room_num);

--Delete from guest_room
DELETE FROM guest_room WHERE guest_id = :guest_id and room_num = :room_num;

-- I did not put update queries in for either guest_room or reservation_room because I felt
-- that they were not necessary and to properly identify an entry in either table you need 
-- all the properties of each entry. Seems reasonable to delete the entry and insert a new
-- one if necessary.

--Read reservation_room table
SELECT * FROM reservation_room;

--Delete from reservation_room table
DELETE FROM reservation_room WHERE reservation_id =:reservation_id and room_num = :room_num;
