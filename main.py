# -*- coding: utf-8 -*-
from    __future__      import unicode_literals
from    flask           import Flask, render_template, json, request, redirect, session, abort, jsonify
from    werkzeug        import generate_password_hash, check_password_hash
from    io_lib          import io_debug
from    io_lib          import io_mysql
from    firebase_admin  import messaging, credentials 
import  firebase_admin
import  os
import  re
import  uuid
import  argparse
import  flask
import  logging

# Private key is not shared
from io_lib import io_credentials as compendium_credentials
compendium_private_key = compendium_credentials.compendium_private_key

# This is necessary for the connection to mysql to support special characters
import sys
from re import search
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
app.secret_key = compendium_credentials.app_secret_key
app.debug = True

# defult initialization for objects.
# currently doing a verbose mode for unittest, will try
# to control these from unittest later.
io_print = io_debug.io_debug(True, None).io_print
database = io_mysql.io_mysql(True, None, True)
# database.configure_credentials('root', 'password', 'compendium')

# ################################################# MAIN  ###########################
@app.route('/')
def main():
    return render_template('index.html')
# ################################################# MAIN  ###########################

# First page, before userhome
@app.route('/home')
def home():

    return render_template('index.html')

# First page, before userhome
@app.route('/license')
def license():

    return render_template('license.html')


# About page
@app.route('/about')
def about():

    return render_template('about.html')


# Sign UP button calls POST
@app.route('/signUp',               methods=['POST','GET'])
def signUp():

    if   request.method == 'GET': 
        name       = request.args.get('example')

    elif request.method == 'POST':

        key        = request.form['key']
        name       = request.form['name']
        email      = request.form['email']
        password   = request.form['password']
        description= request.form['description']
        picture_ref= request.form['picture']
        latitude   = float(request.form['latitude'])
        longitude  = float(request.form['longitude'])
        city       = request.form['city']
        picture    = request.form['picture']

    if key != compendium_private_key:
            return ("Error in Compendium Authentication key " + key)

    try:
        # Validate the received values
        if name and email and password:
            # MySQL process
            database.connect()

            if password != 'password':
                password = generate_password_hash(password)

            result = database.sp_create_user(name,email,password, description,latitude,longitude, city, picture)
            
            if result != 'Error':
                io_print("Successfully created a new user in DB...")
                # return 'Successfully registered ' + name + ' with email: ' + email
                return name

            # User is already in database, since this is the same fuction to log in or sign up from FB, we choose what to do:
            else:
                return result
        else:
            return json.dumps({'html':'<span>Error: Enter the required fields</span>'})
    except Exception as e:
        io_print('Catch signup error: ' + str(e))
        return 'Error: ' + str(e)
    finally:
        if database:
            database.disconnect()

# Profile page
@app.route('/profile',               methods=['POST','GET'])
def profile():

    # GET request
    userName = request.args.get('user')
    userID   = request.args.get('email')

    return render_template('profile.html', name = userName, mail = newmail, data = '{}')


# Exit this session
@app.route('/logout')
def logout():
    return redirect('/')

# Fetch users data
@app.route('/getProfiles',             methods=['GET'])
def getProfiles():

    database.connect()

    data = database.execute('select * from user_info')

    database.disconnect()

    return json.dumps(data)


# Fetch single user's data
@app.route('/getProfile',             methods=['GET'])
def getProfile():

    name       = request.args.get('name')

    database.connect()

    data = database.execute("select * from user_info where facebook_name = '" + name + "'")

    database.disconnect()

    return json.dumps(data)


@app.route('/updateProfile',             methods=['POST','GET'])
def updateProfile():

    try:
        key        = request.form['key']
        user_id    = request.form['user_id']
        name       = request.form['name']
        email      = request.form['email']
        description= request.form['description']
        latitude   = request.form['latitude']
        longitude  = request.form['longitude']
        city       = request.form['city']

        if key != compendium_private_key:
            return ("Error in Compendium Authentication key " + key)

        database.connect()

        query = ("UPDATE user_info SET "
            "user_name = '"       + name        + "' , "
            "user_email = '"      + email       + "' , "
            "description = '"     + description + "' , "
            "city  = '"           + city        + "' , "
            "latitude  = "        + latitude    + " , "
            "longitude = "        + longitude   + " "
            "WHERE user_id = "    + user_id     + ";") 

        data = database.execute(query, True)

        database.disconnect()

        return 'Successfully updated table with the following query: ' + query

    except Exception as e:
        io_print('Catch update profile error: ' + str(e))
        return query + ':Update Error: ' + str(e)
    finally:
        if database:
            database.disconnect()


# Delete User's account
@app.route('/deleteAccount', methods = ['POST'])
def deleteAccount():
	if request.method == 'POST':

		user_name = request.form['user_name']

		try:

			query = "DELETE FROM `user_info` WHERE `user_id` = " + user_name

			database.connect()
			data = database.execute(query, True)

			if not data:
				return "Deleted"
			else:
				return data


		except Exception as e:
			io_print('Delete profile error: ' + str(e))
			return query + ':Delete Error: ' + str(e)

		finally:
			if database:
				database.disconnect()


# Search for string in the database
@app.route('/generalSearch', methods = ['GET'])
def generalSearch():

    if request.method == 'GET':

        try:

            # We receive a series of words and look for the rows whose selected colums contain any of these words
            string = request.args.get('query')
            
            if string != 'ALL':
                query_strings_list = request.args.get('query').split()

                query = "SELECT * FROM user_info WHERE"
                for string in query_strings_list:
                    query = query + " CONCAT(user_name,description,city) like '%" + str(string) + "%' OR" 
                
                # Remove last OR
                query = query[:-2] + "ORDER BY user_name ASC;"

            else:
                query = "SELECT * FROM user_info;"    
            
            database.connect()

            data = database.execute(query)

            return json.dumps(data)

        except Exception as e:
            io_print('Catch update profile error: ' + str(e))
            return query + ':Update Error: ' + str(e)

        finally:
            if database:
                database.disconnect()


# Error handling
@app.route('/error',                methods=['GET','POST'])
def error():
    return render_template('error.html', error = 'TEST ERROR', goTo = "/")


# Start:
# This part is completly ignored by google cloud.
# Just use it for local development.
# Google clound only needs the methods and line 20 to run.
if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(   "-d",
                                "--debug",
                                help="print debug statements",
                                action="store_true",
                                default = False)

    args = args_parser.parse_args()

    IO_DEBUG = args.debug

    io_print = io_debug.io_debug(IO_DEBUG, None).io_print

    database = io_mysql.io_mysql(IO_DEBUG, None, True)

    app.run(host='0.0.0.0',port=5665)
