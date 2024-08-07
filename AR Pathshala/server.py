from flask import Flask, request, redirect,jsonify,render_template,redirect, url_for,send_from_directory
import pymongo
import bcrypt

app = Flask(__name__)

dbconn = pymongo.MongoClient('mongodb://localhost:27017') # Enter your db address
dbname = dbconn['test'] # Enter your db name
dbcollection = dbname['testing'] # Enter your db collection

@app.route('/signup', methods=['POST','GET'])
def signup() -> str:
    if request.method == 'POST':
        full_name = request.form['name']
        # username = request.form['username']
        email_id = request.form['email']
        # phone_number = request.form['phoneNumber']
        password = request.form['password']

        if dbcollection.find_one({'emailId': email_id}):
            return 'Account already exists'

        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        dbcollection.insert_one({'fullName': full_name,'emailId': email_id, 'password': password})
        return 'Successfully created the account. Now you can login to continue'

@app.route('/login', methods=['POST','GET'])
def login() -> str:
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # password = bcrypt.checkpw(password.encode())
        user = dbcollection.find_one({"emailId": email})

        if user and bcrypt.checkpw(password.encode(), user['password']):
            # return redirect('https://www.google.co.in/')# Can only be used for hosted websites.
            # return redirect(url_for('static', filename='index.html'))
            return send_from_directory('.','index.html')
            # return render_template('index.html')
            # return 'Login Successful!'
        else:
            return 'Invalid username or password !!'    

app.run(port=80,host='0.0.0.0')
