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

@webapp.route('/home')
def home():
    return render_template('home.html');

@webapp.route('/book')
def book():
    return render_template('booking.html');

@webapp.route('/index')
def index():
    return render_template('index.html');

@webapp.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == "POST" and "reserve" in request.form:
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

    elif request.method == "POST" and "price" in request.form:
        room = request.form['room']
        types = request.form['type']
        guests = request.form['guests']
        price = request.form['price']

        db_connection = connect_to_database()

        query = 'insert into room (room_num, room_type, max_guests, price) values (%s,%s,%s,%s)'
        data = (room, types, guests, price)
        execute_query(db_connection, query, data)
        return render_template('admin.html')

    else: 
        return render_template('admin.html');
