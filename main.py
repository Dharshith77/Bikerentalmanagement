import base64
from flask import Flask,render_template,request,redirect,session,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_bcrypt import Bcrypt
from base64 import b64encode
from flask_login import UserMixin,LoginManager, login_user,login_manager,login_required,logout_user,current_user
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@localhost:1521/xe'
app.secret_key=os.urandom(25)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return Signup.query.get(user_id)
    except Exception as e:
        return None

class Signup(db.Model,UserMixin):
    fullname= db.Column(db.String(30), primary_key=True)
    email= db.Column(db.String(40), unique=True, index=True, nullable=False)
    phonenum = db.Column(db.Integer(), unique=False, nullable=False)
    password = db.Column(db.String(240), unique=False, nullable=False)

    def get_id(self):
        return self.fullname
@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template('homepage.html')
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method=='POST':
        fullname= request.form.get("fullname")
        email= request.form.get("email")
        phonenum = request.form.get("phonenum")
        hashed_password = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
        entry=Signup(fullname=fullname,email=email,phonenum=phonenum,password=hashed_password)
        db.create_all()
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("login"))
    print("REGISTERED SUCCESSFULLY!")
    return render_template('register.html')
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = Signup.query.filter_by(email=email).first()
        if request.form['rad'] == 'admin':
            if user and bcrypt.check_password_hash(user.password, password ):
                login_user(user)
                return redirect(url_for('adminpage'))
            else:
                flash("Bad username or password")
        elif request.form['rad'] == 'user':
            if user and bcrypt.check_password_hash(user.password, password ):

                login_user(user)
                return redirect(url_for('userpage'))

        return "<h1>Wrong username or password</h1>" #if the username or password does not matches
    return render_template('login.html')
@app.route("/adminpage")
@login_required
def adminpage():
    fullname = current_user.fullname
    return render_template('adminpage.html',fullname=fullname)

@app.route("/userpage")
@login_required
def userpage():
    fullname = current_user.fullname
    return render_template('userpage.html',fullname=fullname)

class Bike(db.Model,UserMixin):

    bikename = db.Column(db.String(100), primary_key=True,nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # New column for creation timestamp

@app.route("/addbike", methods=['GET', 'POST'])
@login_required
def addbike():
    if request.method == 'POST':
        bikename = request.form.get("bikename")
        brand = request.form.get("brand")
        year = request.form.get("year")
        price = request.form.get("price")
        description = request.form.get("description")
        img_file = request.files['image_file']
        image_data = img_file.read()
        bike = Bike(bikename=bikename, brand=brand, year=year, price=price, description=description,created_at=datetime.utcnow(),image_data=image_data)

        db.create_all()
        db.session.add(bike)
        db.session.commit()
        print('Bike Added Successfully')

        #return redirect(url_for('bikeinfo'))  # Redirect the user to the bikeinfo page after form submission.

    return render_template('addbike.html')

#to update and delete added bikes from the datebase
@app.route("/updatebike/<string:bikename>", methods=['GET', 'POST'])
@login_required
def update_bike(bikename):
    bike = Bike.query.get_or_404(bikename)

    if request.method == 'POST':
        # Get the new values for the bike attributes from the form
        new_bikename = request.form.get("bikename")
        new_brand = request.form.get("brand")
        new_year = request.form.get("year")
        new_price = request.form.get("price")
        new_description = request.form.get("description")

        # Update the bike attributes if the new values are not empty
        if new_bikename:
            bike.bikename = new_bikename
        if new_brand:
            bike.brand = new_brand
        if new_year:
            bike.year = new_year
        if new_price:
            bike.price = new_price
        if new_description:
            bike.description = new_description

        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('bikeinfo'))

    return render_template('updatebike.html', bike=bike)

@app.route("/deletebike/<string:bikename>", methods=['POST'])
@login_required
def delete_bike(bikename):
    bike = Bike.query.get_or_404(bikename)
    db.session.delete(bike)
    db.session.commit()
    return redirect(url_for('bikeinfo'))

@app.route("/bikeinfo",methods=['GET','POST'])
@login_required
def bikeinfo():
     bikes= Bike.query.order_by(Bike.created_at.desc()).all()
     for bike in bikes:
             encoded_image = base64.b64encode(bike.image_data).decode('utf-8')
             bike.encoded_image = encoded_image
     return render_template('bikeinfo.html', bikes=bikes)
@app.route("/userlist")
@login_required
def userlist():
    return render_template('userlist.html')

class Booked(db.Model,UserMixin):

    bikename = db.Column(db.String(100), primary_key=True,nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
@app.route("/booking",methods=['GET','POST'])
@login_required
def booking():
    if request.method == 'POST':
        bikename = request.form.get("bikename")
        brand = request.form.get("brand")
        year = request.form.get("year")
        price = request.form.get("price")
        description = request.form.get("description")
        existing_booking = Booked.query.filter_by(bikename=bikename).first()
        if existing_booking:
            flash(" You have already booked this bike.")
        else:
            # Bike is not already booked, proceed with booking
            bike = Bike.query.filter_by(bikename=bikename).first()
            if bike:
                image_data = bike.image_data

                booked_bike = Booked(bikename=bikename, brand=brand, year=year, price=price, description=description,
                                     created_at=datetime.utcnow(), image_data=image_data)
                db.create_all()
                db.session.add(booked_bike)
                db.session.commit()
                flash("Bike booked successfully!")
        return redirect(url_for('booking'))
    bikes= Bike.query.order_by(Bike.created_at.desc()).all()
    for bike in bikes:
        encoded_image = base64.b64encode(bike.image_data).decode('utf-8')
        bike.encoded_image = encoded_image
    return render_template('booking.html', bikes=bikes)

@app.route("/bookingreq",methods=['GET'])
@login_required
def bookingreq():
        booked_bikes = Booked.query.order_by(Booked.created_at.desc()).all()

        for booked_bike in booked_bikes:
             booked_bike.encoded_image = base64.b64encode(booked_bike.image_data).decode('utf-8')

        return render_template('bookingreq.html',  booked_bikes=booked_bikes)


@app.route("/logout",methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == "__main__":

    app.run(debug=True)


