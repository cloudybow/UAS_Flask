from app import db
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

class tbcustomer(db.Model):
    __tablename__ = 'tbcustomer'
    customerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def __init__(self, customerID, name, email, username, password):
        self.customerID = customerID
        self.name = name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password) 

    def __repr__(self):
        return '[%s, %s, %s, %s, %s]' % \
        (self.customerID, self.name, self.email, self.username, self.password)

class tbroom(db.Model):
    __tablename__ = 'tbroom'
    roomID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    def __init__(self, roomID, name, price, stock):
        self.roomID = roomID
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return '[%s, %s, %s, %s]' % \
        (self.roomID, self.name, self.price, self.stock)

class tbcheck(db.Model):
    __tablename__ = 'tbcheck'
    checkID = db.Column(db.Integer, primary_key=True)
    rentID = db.Column(db.Integer, ForeignKey('tbrent.rentID'))
    staffID = db.Column(db.Integer, ForeignKey('tbstaff.staffID'))
    check_in_date = db.Column(db.DateTime)
    check_out_date = db.Column(db.DateTime)

    def __init__(self, checkID, rentID, staffID, check_in_date, check_out_date):
        self.checkID = checkID
        self.rentID = rentID
        self.staffID = staffID
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date

    def __repr__(self):
        return '[%s, %s, %s, %s, %s]' % \
        (self.checkID, self.rentID, self.staffID, self.check_in_date, self.check_out_date)        

class tbstaffrole(db.Model):
    __tablename__ = 'tbstaffrole'
    roleID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, roleID, name):
        self.roleID = roleID
        self.name = name

    def __repr__(self):
        return '[%s, %s]' % \
        (self.roleID, self.name)

class tbstaff(db.Model):
    __tablename__ = 'tbstaff'
    staffID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.Integer)
    password = db.Column(db.Integer)
    roleID = db.Column(db.Integer, ForeignKey('tbstaffrole.roleID'))

    def __init__(self, staffID, name, username, password, roleID):
        self.staffID = staffID
        self.name = name
        self.username = username
        self.password = password
        self.roleID = roleID

    def check_password(self, password):
        return check_password_hash(self.password, password) 

    def __repr__(self):
        return '[%s, %s, %s, %s, %s]' % \
        (self.staffID, self.name, self.username, self.password, self.roleID)

class tbrent(db.Model):
    __tablename__ = 'tbrent'
    rentID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, ForeignKey('tbcustomer.customerID'))
    roomID = db.Column(db.Integer, ForeignKey('tbroom.roomID'))
    date_stamp = db.Column(db.Date)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)
    price = db.Column(db.Integer)
    day = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    total = db.Column(db.Integer)

    def __init__(self, rentID, customerID, roomID, date_stamp, date_from, date_to, price, day, amount, total):
        self.rentID = rentID
        self.customerID = customerID
        self.roomID = roomID
        self.date_stamp = date_stamp
        self.date_from = date_from
        self.date_to = date_to
        self.price = price
        self.day = day
        self.amount = amount
        self.total = total

    def __repr__(self):
        return '[%s, %s, %s, %s, %s, %s, %s, %s, %s, %s]' % \
        (self.rentID, self.customerID, self.roomID, self.date_stamp, self.date_from, self.date_to, self.price, self.day, self.amount, self.total)