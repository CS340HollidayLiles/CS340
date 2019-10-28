from flask import Flask, render_template
from flask import request, redirect
#from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!";

@webapp.route('/guestInformation')
def guestInformation():
    #oForm = forms.EnterGuestInfo()
    #info = models.Information()

    #if request.method == "POST":
    #    db.session.add(info)
    #    db.session.commit()
    #    return render_template ('guestInformation.html', info=info)
    #else:
    return render_template('guestInformation.html');#, Form=oForm)

@webapp.route('/payment')
def payment():
    #oForm = forms.EnterPayment()
    #info = models.Information()

    #if request.method == "POST":
    #    db.session.add(info)
    #    db.session.commit()
    #    return render_template ('payment.html', info=info)
    #else:
    return render_template('payment.html');#, Form=oForm)

@webapp.route('/confirmation')
def confirmation():
    #oForm = forms.ShowConfirmation()
    #info = models.Information()

    #if request.method == "POST":
    #    db.session.add(info)
    #    db.session.commit()
    #    return render_template ('confirmation.html', info=info)
    #else:
    return render_template('confirmation.html');#, Form=oForm)

@webapp.route('/index')
def index():
    return render_template('index.html');

@webapp.route('/booking')
def booking():
    return render_template('booking.html');

@webapp.route('/home')
def home():
    return render_template('home.html');
