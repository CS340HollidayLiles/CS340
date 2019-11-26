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
SELECT room.room_type, room.max_guests, room.price AS RoomType, MaxGuests, Price
WHERE room.room_num NOT IN
( 
   SELECT room_num FROM reservation r
   INNER JOIN room ON reservations.room_num = room.room_num
   WHERE (check_in_input <= r.check_in AND check_out_input >= r.check_out)
      OR (check_in_input < r.check_out AND check_out >= r.check_out)
      OR (r.check_in <= check_in AND r.check_out >= check_in_input)
  AND num_guests_input < room.max_guests
);

