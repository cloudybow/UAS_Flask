from asyncio.windows_events import NULL
from flask import Flask,request,render_template,session,redirect,url_for,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import os
import pdfkit
from flask_mail import Mail, Message

app = Flask(__name__, template_folder="views")
app.config['SECRET_KEY'] = '@#$123456&*()'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/dbhotel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PDF_FOLDER'] = os.path.realpath('.')+'/static/pdf'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app)
mail = Mail(app)
from model import tbcheck, tbroom,tbcustomer,tbrent,tbstaff,tbstaffrole

#CUSTOMER#
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='OTEL.COM',
        year=datetime.now().year,
    )

@app.route('/OTEL.COM-film')
def film():
    return render_template(
        'hotel.html',
        title='List Of Movie',
        year=datetime.now().year,
        message='Your application description page.'
     )

@app.route('/OTEL.COM-contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', year=datetime.now().year)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #get init data from username
        custData = tbcustomer.query.filter_by(username = username).first()
        if(custData is None):
            return render_template('login.html', msg="Wrong Username/Password!")
        else:
            #check if pass is true
            custPass = custData.check_password(password)
            print(custPass)
            if(custPass is False):
                session['loggedin'] = True
                session['role']='customer'
                session['custID'] = custData.customerID
                return redirect(url_for('home'))
            else:
                return render_template('login.html', msg="Wrong Username/Password!",title='Login',year=datetime.now().year)

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        #get the last id of customer
        last_id = tbcustomer.query.order_by(tbcustomer.customerID.desc()).first()
        last_id = last_id.customerID
        #adding data to tbcustomer
        custData = tbcustomer(last_id+1, 
            request.form.get('name'),
            request.form.get('email'),
            request.form.get('username'),
            request.form.get('password'))
        db.session.add(custData)
        db.session.commit()
        print('Data added!')

        return render_template('login.html')

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('role', None)
   session.pop('custID', None)
   # Redirect to login page
   return redirect(url_for('home'))

@app.route('/room', methods=['GET'])
def allRoom():
    roomData = tbroom.query.all()
    return render_template('room.html', data=roomData, year=datetime.now().year)

@app.route('/room/<id>', methods=['POST','GET'])
def room(id):
    roomData = tbroom.query.filter_by(roomID = id).first()
    print(type(roomData))
    #get hotel room data
    if request.method == 'GET':
        if "msg" in session:
            msg = session['msg']
        else:
            msg = ""
        return render_template('roomDetail.html', data=roomData, msg = msg)
    
    #book request
    if request.method == 'POST':
        data = roomData.__dict__
        data.pop('_sa_instance_state', None)

        roomFrom = datetime.strptime(request.form.get('date_from'), '%Y-%m-%d')
        roomTo = datetime.strptime(request.form.get('date_to'), '%Y-%m-%d')
        diff = roomTo - roomFrom
        roomDay = diff.days
        print(type(roomDay))
        roomAmount = request.form.get('room_amount')
        roomTotal = roomData.price * int(roomDay) * int(roomAmount)
        session['book_data'] = {
            'roomData':data,
            'roomFrom': roomFrom,
            'roomTo': roomTo,
            'roomDay':roomDay,
            'roomAmount':roomAmount,
            'roomTotal':roomTotal
        }
        return render_template('roomBooking.html', data=session["book_data"], access=True)

@app.route('/room/book', methods=['POST'])
def roomBook():
    bookData = session["book_data"]
    roomData = bookData['roomData']
    print(bookData)

    #adding new rent
    #get last id of rent
    last_id = tbrent.query.order_by(tbrent.rentID.desc()).first()
    #get cust id from rent
    if 'custID' in session:
        customerID = session['custID']
        #init data
        rentID = last_id.rentID + 1
        roomID = roomData['roomID']
        date_stamp = date.today()
        date_from = bookData['roomFrom']
        date_to = bookData['roomTo']
        price = roomData['price']
        day = bookData['roomDay']
        amount = bookData['roomAmount']
        total = bookData['roomTotal']

        data = tbrent(rentID, customerID, roomID, date_stamp, date_from, date_to, price, day, amount, total)
        db.session.add(data)
        db.session.commit()
        print("data added")

        session['msg'] = "Data added successfully!"
        return redirect(url_for('allRoom'))
    else:
        return render_template('roomDetail.html', msg="Booking is Unavailable. Login First!")

#STAFF#
@app.route('/staff_login', methods=['GET','POST'])
def staffLogin():
    if request.method == 'GET':
        return render_template('loginadmin.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #get init data from username
        staffData = tbstaff.query.filter_by(username = username).first()
        if(staffData is None):
            return render_template('loginadmin.html', msg="Wrong Username/Password!")
        else:
            # #check if pass is true
            # staffPass = staffData.check_password(password)
            # print(staffPass)
            session['loggedin'] = True
            session['role']='admin'
            session['staffID'] = staffData.staffID
            return redirect(url_for('dashboard'))

@app.route('/login/logoutadmin')
def logoutadmin():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('role', None)
   session.pop('staffID', None)
   # Redirect to login page
   return redirect(url_for('staffLogin'))

@app.route('/staffregis', methods=['POST','GET'])
def staffregister():
    if request.method == 'GET':
        role_list = tbstaffrole.query.all()
        return render_template('newadmin.html', role_list=role_list)
    
    if request.method == 'POST':
        #get the last id of staff
        last_id = tbstaff.query.order_by(tbstaff.staffID.desc()).first()
        last_id = last_id.staffID
        #adding data to tbstaff
        staffData = tbstaff(last_id+1, 
            request.form.get('name'), 
            request.form.get('username'), 
            request.form.get('password'), 
            request.form.get('roleID'))
        db.session.add(staffData)
        db.session.commit()
        print('Data added!')

        return render_template('login.html')

@app.route('/OTEL.COM-dashboard')
def dashboard():
    if 'loggedin' in session:
        # User is loggedin show them the home page
        data = tbstaff.query.filter_by(staffID = session['staffID']).first()
        return render_template('dashboard.html', staffID=session['staffID'], tbstaff=data, title='Dashboard',year=datetime.now().year)
    return redirect(url_for('staffLogin'))

@app.route('/dashboard/booking', methods=['GET'])
def booking():
    if 'staffID' in session:
        #rent page#
        rentData = tbrent.query.all()
        staffName = tbstaff.query.filter_by(staffID = session['staffID']).first()
        staffName = staffName.name
        #array for report dropdown
        dropdown_data = [{'name':'Rent'},{'name':'Check-In'}]
        return render_template('staff_Checkin.html', data=rentData, dropdown_data=dropdown_data, staffName=staffName)
    else:
        return render_template('staff_login.html')

@app.route('/dashboard/booking/<req>/<rentID>', methods=['GET'])
def bookingCheck(req, rentID):
    #need session for STAFF ROLE ID
    if 'staffID' in session:
        staffID = session["staffID"]
    
        #get room id of current rent
        rentData = tbrent.query.filter_by(rentID = rentID).first()
        #targeted room row
        roomData = tbroom.query.filter_by(roomID = rentData.roomID).first()

        if req == 'checkin':
            #get last id of rent
            last_id = tbcheck.query.order_by(tbcheck.checkID.desc()).first()
            last_id = last_id.checkID
            #create new data in check table
            checkData = tbcheck((last_id+1), rentID, staffID, datetime.now(), NULL)
            db.session.add(checkData)
            db.session.commit()

            #remove stock
            roomData.stock -= 1
            db.session.merge(roomData)
            db.session.commit()
            print("checkin is done!")

        elif req == 'checkout':
            #get checkin data
            checkData = tbcheck.query.filter_by(rentID = rentID).first()

            if checkData:
                #update checkout column
                checkData.check_out_date = datetime.now()
                db.session.merge(checkData)
                db.session.commit()

                #return room stock
                roomData.stock +=1
                db.session.merge(roomData)
                db.session.commit()
                print('checkout is done!')
        return redirect(url_for('booking'))
    else:
        return render_template('staff_login.html')

@app.route('/dashboard/get_report', methods=['POST'])
def getReport():
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    selected = request.form.get('selected')

    if selected == 'Rent':
        if date_from != None or date_to != None:
            rentData = tbrent.query.filter(tbrent.date_stamp.between(date_from, date_to)).all()
        elif date_to == None:
            rentData = tbrent.query.filter_by(date_stamp = date_from).all()
        else:
            return render_template('getreport.html')

        rendered = render_template("rent_data.html", data=rentData, date_from=date_from, date_to=date_to)
        config = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        pdf = pdfkit.from_string(rendered, configuration = config)
        filename = 'report.pdf'

        response = make_response(pdf)
        response.headers['Content-Type'] = "templates"
        response.headers['Content-Disposition'] = 'attachment;filename=' + filename
        return response

    if selected == 'Check-In':
        date_from = date_from + ' 00:00:00'
        date_to = date_to + ' 23:59:59'

        if date_from != None or date_to != None:
            checkData = tbcheck.query.filter((tbcheck.check_in_date >= date_from) & (tbcheck.check_in_date <= date_to)).all()
            rendered = render_template("checkin_data.html", data=checkData, date_from=date_from, date_to=date_to)
            config = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
            pdf = pdfkit.from_string(rendered, configuration = config)
            filename = 'report.pdf'

            response = make_response(pdf)
            response.headers['Content-Type'] = "templates"
            response.headers['Content-Disposition'] = 'attachment;filename=' + filename
            return response
        else:
            return render_template('getreport.html')

@app.route('/dashboard/advertisement_mail', methods=['GET', 'POST'])
def admail():
    if request.method == 'GET':
        return render_template('staff_advertisement.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        subject = request.form['subject']
        message = request.form['message']

        app.config['MAIL_USERNAME'] = email
        app.config['MAIL_PASSWORD'] = password

        #fetch all customer
        cust = tbcustomer.query.all()
        #sending in bulk
        with mail.connect() as conn:
            for d in cust:
                msg = Message(subject,
                recipients=[d.email],
                body=message,
                sender = email)
                conn.send(msg)

if __name__ == '__main__':
    app.run(debug=True)