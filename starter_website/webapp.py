from flask import Blueprint, Flask, render_template
from flask import request, redirect
import random
import os.path
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!";

@webapp.route('/guestInformation', methods=['POST', 'GET'])
def guestInformation():
    #oForm = forms.EnterGuestInfo()
    #info = models.Information() 

    if request.method == "POST":
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        code = request.form['area_code']
        num = request.form['phone_number']
        reservation = request.form['reservation']
        room_num = request.form['room']
        db_connection = connect_to_database()

        query = 'insert into guest (reservation_id, f_name, l_name, area_code, phone_number) values (%s,%s,%s,%s,%s)'
        query2 = 'select last_insert_id()'
        query3 = 'update reservation set guest_id = %s where reservation_id = %s'
        query4 = 'insert into guest_room (guest_id, room_num) values (%s, %s)'

        data = (reservation, f_name, l_name, code, num)
        result = execute_query(db_connection, query, data)

        result = execute_query(db_connection, query2)

        guest_id = result.fetchall()[0][0]

        data = (guest_id, reservation)
        result = execute_query(db_connection, query3, data)

        data = (guest_id, room_num)
        result = execute_query(db_connection, query4, data)

        return render_template('payment.html', data=reservation)

    else:
        return render_template('guestInformation.html')#, Form=oForm)

@webapp.route('/payment', methods=['POST', 'GET'])
def payment():
    #oForm = forms.EnterPayment()
    #info = models.Information()

    if request.method == "POST":
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        types = request.form['types']
        cc_num = request.form['cc_num']
        cc_code = request.form['code']
        house = request.form['house_number']
        street = request.form['street_name']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        country = request.form['country']
        reservation = request.form['reservation']
        r = reservation[0:2]

        db_connection = connect_to_database()

        query = 'insert into payment (reservation_id, f_name, l_name, cc_type, cc_num, cc_security_code, house_num, street, city, state, zip_code, country, total_charged) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        query2 = 'select last_insert_id()'
        query3 = 'update reservation set payment_id = %s where reservation_id = %s'
        
        data = (r, f_name, l_name, types, cc_num, cc_code, house, street, city, state, zip_code, country, 94.75)
        execute_query(db_connection, query, data)

        result = execute_query(db_connection, query2)

        payment = result.fetchall()[0][0]
        data = (payment, r)
        execute_query(db_connection, query3, data)

        query4 = 'select room_num, check_in, check_out, num_guests, confirmation_num, guest_id from reservation where reservation_id = %s'
        data = (r,)
        result = execute_query(db_connection, query4, data).fetchall()
        room_num = result[0][0]
        print(room_num)
        res_data = [result[0][1], result[0][2], result[0][3], result[0][4]]

        query6 = 'select f_name, l_name from guest where guest_id = %s'
        result = execute_query(db_connection, query6, (result[0][5],)).fetchall()
        guest_data = [result[0][0], result[0][1]]

        query5 = 'select room_type from room where room_num = %s'
        result = execute_query(db_connection, query5, (room_num,)).fetchall()
        room_data = [room_num, result[0][0]]

        payment_data = [f_name, l_name, cc_num, house, street, city, state, zip_code, country, 94.75]

        print(res_data)
        print(payment_data)
        print(room_data)
        return render_template('confirmation.html', res = res_data, room = room_data, payment = payment_data, guest = guest_data)
    else:
        return render_template('payment.html')#, Form=oForm)

@webapp.route('/confirmation')
def confirmation():

    return render_template('confirmation.html')

@webapp.route('/home', methods=['GET'])
def home():
    if request.args.get('Check'):
        print("here")
        db_connection = connect_to_database()

        c_in = request.args['c/i']
        c_out = request.args['c/o']
        guests = request.args['guest']

        query = 'select * from room where max_guests >= %s and room_num not in (select distinct room.room_num from room join reservation_room on room.room_num = reservation_room.room_num join reservation on reservation_room.reservation_id = reservation.reservation_id where ((DATE %s < check_in and DATE %s >= check_in) or (DATE %s >= check_in and DATE %s <= check_out)))'

        data = (guests, c_in, c_out, c_in, c_in)

        result = execute_query(db_connection, query, data)

        print("hi")

        print(result)

        return render_template('booking.html', room=result, reserve=data);

    else:
        print("okay")
        return render_template('home.html');

@webapp.route('/book', methods=['GET', 'POST'])
def book(): 
    
    if request.method == 'POST':
        db_connection = connect_to_database() 

        c_in = request.form.get('in')
        c_out = request.form.get('out')
        guests = request.form.get('guests')
        room = request.form.get('room_num')
        confirmation = random.randrange(1000000000)

        query = 'insert into reservation (room_num, check_in, check_out, num_guests, confirmation_num) values (%s, %s, %s, %s, %s)'
        query2 = 'select last_insert_id()'

        query3 = 'insert into reservation_room (room_num, reservation_id) values (%s, %s)'

        data = (room, c_in, c_out, guests, confirmation)

        result = execute_query(db_connection, query, data)
        result = execute_query(db_connection, query2)

        reservation = result.fetchall()[0][0]

        data = (room, reservation)
        result = execute_query(db_connection, query3, data)

        print(c_in)
        print(c_out)
        print(guests)
        print(room)
        print(reservation)

        return render_template('guestInformation.html', reserve=reservation, room_num=room)

    else:

        if request.args.get('Search'):
            print("here")
            db_connection = connect_to_database()

            c_in = request.args.get('c_i')
            c_out = request.args.get('c_o')
            guests = request.args.get('guest')

            query = 'select * from room where max_guests >= %s and room_num not in (select distinct room.room_num from room join reservation_room on room.room_num = reservation_room.room_num join reservation on reservation_room.reservation_id = reservation.reservation_id where ((DATE %s < check_in and DATE %s >= check_in) or (DATE %s >= check_in and DATE %s <= check_out)))'

            data = (guests, c_in, c_out, c_in, c_in)

            result = execute_query(db_connection, query, data)

            print("hi")

            print(result)

            return render_template('booking.html', room=result, reserve=data);

        else:
            print("okay")
            reserve = None
            return render_template('booking.html', reserve=reserve);

@webapp.route('/index')
def index():
    return render_template('index.html');

@webapp.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "GET":
        print("MySQL Results")
        db_connection = connect_to_database()
        
        query1 = 'select * from room'
        roomresult = execute_query(db_connection, query1)
        print(roomresult)
        query2 = 'select * from guest'
        guestresult = execute_query(db_connection, query2)
        print(guestresult)
        
        query3 = 'select * from reservation'
        reservationresult = execute_query(db_connection, query3)
        print(reservationresult)
        
        query4 = 'select * from payment'
        paymentresult = execute_query(db_connection, query4)
        print(paymentresult)
        
        return render_template('admin.html', room=roomresult, guest=guestresult, reservation=reservationresult, payment=paymentresult)


    else:
        if "UpdateGuest" in request.form:
            print("Update guest")
            guest = request.form['guest_id']
            reserve = request.form['reserve']
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            area = request.form['area_code']
            extension = request.form['phone_number']

            db_connection = connect_to_database()

            query = 'update guest set reservation_id = %s, f_name = %s, l_name = %s, area_code = %s, phone_number = %s where guest_id = %s'
            data = (reserve, f_name, l_name, area, extension, guest)
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "DeleteGuest" in request.form:
            print("Delete guest")
            num = request.form['guest_id']
            db_connection = connect_to_database()
            query = 'delete from guest where guest_id = (%s)'
            data = (num, )
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "UpdatePayment" in request.form:
            print("Update payment")
            payment = request.form['payment_id']
            reserve = request.form['reserve']
            f_name = request.form['f_name']
            l_name = request.form['l_name']
            types = request.form['types']
            cc_number = request.form['cc_number']
            security_code = request.form['security_code']
            house = request.form['house_number']
            street = request.form['street_name']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']
            country = request.form['country']
            total = request.form['total']

            db_connection = connect_to_database()

            query = 'update payment set reservation_id = %s, f_name = %s, l_name = %s, cc_num = %s, cc_type = %s, cc_security_code = %s, house_num = %s, street = %s, city = %s, state = %s, zip_code = %s, country = %s, total_charged = %s where payment_id = %s'
            data = (reserve, f_name, l_name, cc_number, types, security_code, house, street, city, state, zip_code, country, total, payment)
            execute_query(db_connection, query, data)

            return render_template('admin.html')

        elif "DeletePayment" in request.form:
            print("Delete payment")
            num = request.form['payment_id']
            db_connection = connect_to_database()
            query = 'delete from payment where payment_id = (%s)'
            data = (num, )
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "AddReservation" in request.form:
            print("insert reservation")
            reserve = request.form['reserve']
            guest = request.form['guest']
            payment = request.form['payment']
            room = request.form['room']
            check_in = request.form['check_in']
            check_out = request.form['check_out']
            num = request.form['num']
            confirm = request.form['confirm']

            db_connection = connect_to_database()

            query = 'insert into reservation (guest_id, payment_id, room_num, check_in, check_out, num_guests, confirmation_num) values (%s,%s,%s,%s,%s,%s,%s)'
            data = (guest, payment, room, check_in, check_out, num, confirm)
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "UpdateReservation" in request.form:
            print("update reservation")
            reserve = request.form['reserve']
            guest = request.form['guest']
            payment = request.form['payment']
            room = request.form['room']
            check_in = request.form['check_in']
            check_out = request.form['check_out']
            num = request.form['num']
            confirm = request.form['confirm']

            db_connection = connect_to_database()

            query = 'update reservation set guest_id = %s, payment_id = %s, room_num = %s, check_in = %s, check_out = %s, num_guests = %s, confirmation_num = %s where reservation_id = %s'
            data = (guest, payment, room, check_in, check_out, num, confirm, reserve)
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "DeleteReservation" in request.form:
            print("delete reservation")
            num = request.form['reserve']
            print("NUM:" + num)
            db_connection = connect_to_database()
            query = 'delete from reservation where reservation_id = (%s)'
            data = (num, )
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "AddRoom" in request.form:
            print("insert room")
            room = request.form['room']
            types = request.form['type']
            guests = request.form['guests']
            price = request.form['price']

            db_connection = connect_to_database()

            query = 'insert into room (room_num, room_type, max_guests, price) values (%s,%s,%s,%s)'
            data = (room, types, guests, price)
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "UpdateRoom" in request.form:
            print("update room")
            room = request.form['room']
            types = request.form['type']
            guests = request.form['guests']
            price = request.form['price']

            db_connection = connect_to_database()

            query = 'update room set room_type = %s, max_guests = %s, price = %s where room_num = %s'
            data = (types, guests, price, room)
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        elif "DeleteRoom" in request.form:
            print("delete room")
            num = request.form['room']
            db_connection = connect_to_database()
            query = 'delete from room where room_num = (%s)'
            data = (num, )
            execute_query(db_connection, query, data)
            return render_template('admin.html')

        else:

            print("else")
            return render_template('admin.html')
