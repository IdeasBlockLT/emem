# -*- coding: utf-8 -*-
from    __future__      import unicode_literals
from    flask           import Flask, render_template, json, request, redirect, session, abort, jsonify
# from    werkzeug        import generate_password_hash, check_password_hash
from    io_lib          import io_debug
# from    io_lib          import io_mysql
import  os
import  re
import  uuid
import  argparse
import  flask
import  logging

# Private key is not shared
# from io_lib import io_credentials as compendium_credentials
compendium_credentials = "keykeykeykey"
compendium_private_key = "keykeykeykey"
# compendium_private_key = compendium_credentials.compendium_private_key

# This is necessary for the connection to mysql to support special characters
import sys
from re import search

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/Uploads'
# app.secret_key = compendium_credentials.app_secret_key
app.secret_key = compendium_private_key
app.debug = True

# defult initialization for objects.
# currently doing a verbose mode for unittest, will try
# to control these from unittest later.
# io_print = io_debug.io_debug(True, None).io_print
# database = io_mysql.io_mysql(True, None, True)
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
@app.route('/prog')
def prog():

    infile = open("static/texts/emem_table.csv","r")

    table = []

    for line in infile:
        row = line.split(";")
        table.append(row)

    return render_template('program.html')#, data = table)


# About page
@app.route('/about')
def about():

    infile = open("static/texts/emem_table.csv","r")

    table = []

    for line in infile:
        row = line.split(";")
        table.append(row)

    return render_template('program.html', data = table)




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

    # database = io_mysql.io_mysql(IO_DEBUG, None, True)

    app.run(host='0.0.0.0',port=5665)
