#!/usr/bin/python3

import json
import requests
from flask import Flask, render_template, request
from flask_login import current_user
from flask_mongoengine import MongoEngine
from wtforms import Form, BooleanField, TextField, PasswordField, IntegerField, StringField, validators
from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required, RegisterForm

app = Flask(__name__)

# MongoDB Config
app.config['MONGODB_DB'] = 'getofftheroad_db'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['SECRET_KEY'] = '9585hjg983883'
app.config['AUTH_USER_REGISTRATION'] = True

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

# Create database connection object
db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    first_name = db.StringField(max_length=254)
    location_code = db.IntField()
    phone_number = db.IntField(min_length=10, max_length=10)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

class CustomRegisterForm(RegisterForm):
    first_name = TextField('First Name', [validators.Length(min=4, max=20)])
    #email = TextField('Email Address', [validators.Length(min=6, max=50)])
    #password = PasswordField('New Password', [
    #    validators.Required(),
    #    validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    location_code = IntegerField('Zip Code', [validators.Length(min=5, max=5)])
    phone_number = StringField('Phone Number')

    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])
                                

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=CustomRegisterForm)

# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='cwilkin@protonmail.com', password='password')

@app.route('/')
def index():
    return render_template("index.html", loggedIn=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomRegisterForm()
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey = User(form.first_name.data, form.email.data, hashpass, form.location_code.data, form.phone_number.data).save()
                login_user(hey)
                return redirect('/')
    return render_template('security/register_user.html', form=form)

"""
@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('security/register_user.html')
"""
@app.route('/api/v1.0/demo', methods=['GET'])
def demo():

    codes = request.args.get('location')
    

    return "Load" + str(codes)


@app.route('/api/v1.0/search', methods=['GET'])
def search():

    codes = request.args.get('location')
    APIKEY = "qEDtcGHcyGVGAcUKA9NbSFcNTkWPPnyU"
    
    URL = "http://dataservice.accuweather.com/locations/v1/cities/search"

    PARAMS = {'apikey':APIKEY,
            'q':codes
            }

    r = requests.get(url = URL, params = PARAMS)

    data = r.json()

    out = []

    for result in data:
        reg = result['Region']['ID']
        if reg != 'NAM':
            continue
        outresult = {}
        outresult['code'] = result['Key']
        outresult['city'] = result['LocalizedName']
        outresult['zip'] = result['PrimaryPostalCode']
        outresult['state'] = result['AdministrativeArea']['LocalizedName']
        
        out.append(outresult)
    return json.dumps(out)

@app.route('/api/v1.0/drivability', methods=['GET'])
def get_tasks():
    return "Today is a beautiful day. 10/10"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
