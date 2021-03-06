from flask import Flask, redirect, request, session, url_for, render_template
from flask_restful import *
from bson.json_util import loads, dumps
import bcrypt
from SeniorProject.database import conn_DB
from SeniorProject.resources.reservation import Reservation
from SeniorProject.resources.user import User

app = Flask(__name__)
api = Api(app)

db = conn_DB()


@app.route('/')
@app.route('/home')
def home():
    return 'This is a page. I made this :)'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Login_Page.html')
    else:
        data = request.form
        users = db.users
        login_user = users.find_one({'username': data.get('username')})  # find user in db

        if login_user:  # if login user exists check hashed pass
            if bcrypt.hashpw(data.get('password').encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = data.get('username')
                #return redirect(url_for('home'))
                return "success"

        else:
            return 'Invalid username/password combination'


@app.route('/register', methods=['GET'])
def register():
    # load template, then pass info to User resource to POST new user
    # session['username'] = request.json['username']  # session retruned user

@app.route('/calendar', methods=['GET'])
def calendar():

    
api.add_resource(Reservation, '/reservations')
api.add_resource(User, '/users', '/users/<id>')
api.add_resource(Room, '/rooms', '/rooms/<id>')

if __name__ == '__main__':
    app.run(debug=True)
