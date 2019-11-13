#Add Guest
INSERT INTO guest (f_name, l_name, area_code, phone_number) VALUES (:f_name_input, :l_name_input, :area_code_input, :phone_number_input)

#Update Guest
UPDATE guest SET f_name = :f_name_input,  l_name = :l_name_input, area_code= :area_code_input,  phone_number= :phone_number_input WHERE id=:guest_Id_input

#Delete Guest
DELETE FROM guest WHERE id = :guest_Id_from_update_form

#Read Entire uest Table
SELECT * FROM guest

#Add Room
INSERT INTO room (room_num, room_type, pets_allowed, max_guests, price) VALUES (:room_num_input, :room_type_input, :pets_allowed_input, :max_guests_input, price_input)

#Update Room
UPDATE room SET room_num= :room_num_input, room_type= :room_type_input, pets_allowed= :pets_allowed_input, max_guests= :max_guests_input, price= :price_input WHERE room_num= :room_num_input

#Delete Room
DELETE FROM room WHERE id = :room_num_from_update_form

#Read Entire Room Table
SELECT * FROM room

#Add Reservation
INSERT INTO reservation (check_in, check_out, bringing_pets, num_guests, confirmation_num, room_num)  VALUES (:check_in_input, :check_out_input, :bringing_pets_input, :num_guests_input, :generated_confirmation_num, :room_num_from_browse_rooms_form)

#Update Reservation
UPDATE reservation SET check_in= :check_in_input, check_out= :check_out_input, bringing_pets= :bringing_pets_input, num_guests= :num_guests_input, confirmation_num= :generated_confirmation_num, room_num= :room_num_from_browse_rooms_form WHERE id= :reservation_id_from_update_form

#Delete Reservation
DELETE FROM reservation WHERE id = :reservation_id_from_update_form

#Read Entire Reservation Table
SELECT * FROM Reservation

#Add Payment
INSERT INTO payment (f_name, l_name, cc_num, cc_type, cc_security_code, house_num, street_name, city, state, zip_code, country, total_charged) VALUES (:f_name_input, :l_name_input, :cc_num_input, :cc_type_input, :cc_security_code_input, :house_num_input, :street_name_input, :city_input, :state_input, :zip_code_input, :country_input, :total_charged_from_reservation)

#Update Payment
UPDATE payment SET f_name= :f_name_input, l_name= :l_name_input, cc_num=: cc_num_input, cc_type= cc_type_input, cc_security_code= :cc_security_code_input, house_num= :house_num_input, street_name= :street_name_input, city= :city_input, state=: state_input, zip_code= :zip_code_input, country= :country_input, total_charge= :total_charged_from_reservation WHERE id= :payment_id_from_update_form

#Delete Payment
DELETE FROM payment WHERE id = :payment_id_from_update_form

#Read Entire Payment Table
SELECT * FROM payment 

#Check availability button (list open rooms to make a reservation)
SELECT room.room_type, room.max_guests, room.price AS RoomType, MaxGuests, Price
WHERE room.room_num NOT IN
( 
   SELECT room_num FROM reservation r
   INNER JOIN room ON reservations.room_num = room.room_num
   WHERE (check_in_input <= r.check_in AND check_out_input >= r.check_out)
      OR (check_in_input < r.check_out AND check_out >= r.check_out)
      OR (r.check_in <= check_in AND r.check_out >= check_in_input)
  AND num_guests_input < room.max_guests
)
