/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40101 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40101 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40101 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

drop table if exists guest;
/*!40101 set @saved_cs_client   = @@character_set_client */;
/*!40101 set character_set_client = utf8 */;
create table guest (
	guest_id int(11) NOT NULL AUTO_INCREMENT,
	reservation_id int(11) DEFAULT NULL,
	f_name varchar(20) NOT NULL,
	l_name varchar(20) DEFAULT NULL,
	area_code varchar(3) DEFAULT NULL,
	phone_number varchar(12) DEFAULT NULL,
	primary key (guest_id)
) engine=innodb default charset=latin1;
/*!40101 set character_set_client = @saved_cs_client */;

drop table if exists payment;
/*!40101 set @saved_cs_client   = @@character_set_client */;
/*!40101 set character_set_client = utf8 */;
CREATE TABLE payment (
    payment_id int(11) NOT NULL AUTO_INCREMENT,
    reservation_id int(11) DEFAULT NULL,
    f_name varchar(20) NOT NULL,
    l_name varchar(20) DEFAULT NULL,
    cc_num varchar(16) DEFAULT NULL,
    cc_type varchar(20) DEFAULT NULL,
    cc_security_code varchar(20) DEFAULT NULL,
    house_num varchar(20) DEFAULT NULL,
    street varchar(20) DEFAULT NULL,
    city varchar(20) DEFAULT NULL,
    state varchar(2) DEFAULT NULL,
    zip_code varchar(20) DEFAULT NULL,
    country varchar(20) DEFAULT NULL,
    total_charged decimal(5,2) DEFAULT NULL,
    PRIMARY KEY (payment_id)
) engine=innodb default charset=latin1;
/*!40101 set character_set_client = @saved_cs_client */;

drop table if exists reservation;
/*!40101 set @saved_cs_client   = @@character_set_client */;
/*!40101 set character_set_client = utf8 */;
CREATE TABLE reservation (
    reservation_id int(11) NOT NULL AUTO_INCREMENT,
    guest_id int(11) DEFAULT NULL,
    payment_id int(11) DEFAULT NULL,
    room_num int(11) DEFAULT NULL,
    check_in DATE NOT NULL,
    check_out DATE DEFAULT NULL,
    num_guests varchar(3) DEFAULT NULL,
    confirmation_num varchar(12) DEFAULT NULL,
    PRIMARY KEY (reservation_id)
) engine=innodb default charset=latin1;
/*!40101 set character_set_client = @saved_cs_client */;

drop table if exists room;
/*!40101 set @saved_cs_client   = @@character_set_client */;
/*!40101 set character_set_client = utf8 */;
CREATE TABLE room (
    room_num int(11) NOT NULL,
    room_type varchar(20) DEFAULT NULL,
    max_guests int(11) DEFAULT NULL,
    price decimal(5,2) DEFAULT NULL,
    PRIMARY KEY (room_num)
) engine=innodb default charset=latin1;
/*!40101 set character_set_client = @saved_cs_client */;

drop table if exists guest_room;
/*!40101 set @saved_cs_client   = @@character_set_client */;
/*!40101 set character_set_client = utf8 */;
CREATE TABLE guest_room (
    guest_id int(11) NOT NULL,
    room_num int(11) NOT NULL,
    PRIMARY KEY (guest_id, room_num),
    CONSTRAINT gr_fk1 FOREIGN KEY (guest_id) REFERENCES guest  (guest_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT gr_fk2 FOREIGN KEY (room_num) REFERENCES room  (room_num) ON DELETE CASCADE ON UPDATE CASCADE
) engine=innodb default charset=latin1;
/*!40101 set character_set_client = @saved_cs_client */;

drop table if exists reservation_room;
/*!40101 set @saved_cs_client   = @@character_set_client */;
/*!40101 set character_set_client = utf8 */;
CREATE TABLE reservation_room (
    reservation_id int(11) NOT NULL,
    room_num int(11) NOT NULL,
    PRIMARY KEY (reservation_id, room_num),
    CONSTRAINT rr_fk1 FOREIGN KEY (reservation_id) REFERENCES reservation  (reservation_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT rr_fk3 FOREIGN KEY (room_num) REFERENCES room  (room_num) ON DELETE CASCADE ON UPDATE CASCADE
) engine=innodb auto_increment=28 default charset=latin1;
/*!40101 set character_set_client = @saved_cs_client */;

ALTER TABLE guest 
	ADD CONSTRAINT guest_fk1 FOREIGN KEY (reservation_id) REFERENCES reservation (reservation_id) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE payment ADD CONSTRAINT payment_fk1 FOREIGN KEY (reservation_id) REFERENCES reservation (reservation_id) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE reservation
	ADD CONSTRAINT res_fk1 FOREIGN KEY (guest_id) REFERENCES guest  (guest_id) ON DELETE SET NULL ON UPDATE CASCADE,
	ADD CONSTRAINT res_fk2 FOREIGN KEY (payment_id) REFERENCES payment  (payment_id) ON DELETE SET NULL ON UPDATE CASCADE,
	ADD CONSTRAINT res_fk3 FOREIGN KEY (room_num) REFERENCES room  (room_num) ON DELETE SET NULL ON UPDATE CASCADE;

INSERT INTO room (room_num, room_type, max_guests, price) VALUES (101, "Double Queen", 4, 150.00), (204, "Double Queen Suite", 6, 200.00), (146, "King", 2, 175.00), (234, "King Suite", 4, 250.00);

INSERT INTO reservation (guest_id, payment_id, room_num, check_in, check_out, num_guests, confirmation_num)
  VALUES  (NULL, NULL, 101, DATE "2015-12-17", DATE "2015-12-19", "4", "48627"), 
          (NULL, NULL, 146, DATE "2015-11-20", DATE "2015-11-24", "2", "34652"), 
          (NULL, NULL, 234, DATE "2016-01-05", DATE "2016-01-06", "2", "98761"), 
          (NULL, NULL, 204, DATE "2016-01-23", DATE "2016-01-27", "3", "79464");

INSERT INTO guest (reservation_id, f_name, l_name, area_code, phone_number)
  VALUES  (1, "Steve", "Matthews", "503", "594758"), 
          (2, "Helen", "Torres", "888", "423631"), 
          (3, "Ana", "Ballard", "971", "483931"), 
          (4, "Lynn", "Mcgee", "493", "293045");

INSERT INTO payment (reservation_id, f_name, l_name, cc_num, cc_type, cc_security_code, house_num, street, city, state, zip_code, country, total_charged)
  VALUES  (2, "Helen", "Torres", "4951236789465123", "846", "Visa","555", "Lafayette Rd.", "Chester", "PA", "19013", "USA", 136.45), 
          (3, "Ana", "Ballard", "3489516278954621", "897", "MasterCard", "89", "Fifth Rd", "Roswell", "GA", "30075", "USA", 243.50), 
          (1, "Steve", "Matthews", "3950682719503845", "456", "American Express", "904", "Pennington Road", "Butler", "PA", "16001", "USA", 594.32), 
          (4, "Lynn", "Mcgee", "9402859023840532", "256", "Discover", "734", "Tarkiln Hill Drive", "Ashburn", "VA", "20147", "USA", 145.52);

UPDATE reservation SET guest_id = 1, payment_id = 3 WHERE reservation_id = 1;
UPDATE reservation SET guest_id = 2, payment_id = 1 WHERE reservation_id = 2;
UPDATE reservation SET guest_id = 3, payment_id = 2 WHERE reservation_id = 3;
UPDATE reservation SET guest_id = 4, payment_id = 4 WHERE reservation_id = 4;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTRE_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

