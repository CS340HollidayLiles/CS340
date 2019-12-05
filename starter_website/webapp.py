from flask import Blueprint, Flask, render_template
from flask import request, redirect
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

        db_connection = connect_to_database()

        query = 'insert into guest (reservation_id, f_name, l_name, area_code, phone_number) values (%s,%s,%s,%s,%s)'
        data = (28, f_name, l_name, code, num)
        execute_query(db_connection, query, data)
        return render_template('payment.html')

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

        db_connection = connect_to_database()

        query = 'insert into payment (reservation_id, f_name, l_name, cc_type, cc_num, cc_security_code, house_num, street, city, state, zip_code, country, total_charged) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = (28, f_name, l_name, types, cc_num, cc_code, house, street, city, state, zip_code, country, 94.75)
        execute_query(db_connection, query, data)
        return render_template('confirmation.html')
    else:
        return render_template('payment.html')#, Form=oForm)

@webapp.route('/confirmation')
def confirmation():
    #oForm = forms.ShowConfirmation()
    #info = models.Information()

    #if request.method == "POST":
    #    db.session.add(info)
    #    db.session.commit()
    #    return render_template ('confirmation.html', info=info)
    #else:
    return render_template('confirmation.html')#, Form=oForm)

@webapp.route('/home', ['GET'])
def home():
    if "Check" in request.form:
        db_connection = connect_to_database()

        c_in = request.form['c/i']
        c_out = request.form['c/o']
        guests = request.form['guest']

        query = 'select * from room join reservation_room on room.room_num = reservation_room.room_num
        join reservation on reservation_room.reservation_id = reservation.reservation_id where max_guests > %s and
        ((%s < check_in and %s < check_in) or (%s > check_out and %s > check_out))'

        data = (guests, c_in, c_out, c_in, c_out);

        result = execute_query(db_connection, query, data);

        return render_template('booking.html', room=result);

    else:
        return render_template('home.html');

@webapp.route('/book', methods=['GET'])
def book(): 
    return render_template('booking.html');

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
