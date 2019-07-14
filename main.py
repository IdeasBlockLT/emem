# -*- coding: utf-8 -*-
from    __future__      import unicode_literals
from    flask           import Flask, render_template, json, request, redirect, session, abort, jsonify
from    io_lib          import io_debug
import  os
import  re
import  uuid
import  argparse
import  flask
import  logging
# import socket

# Private key is not shared
compendium_credentials = "keykeykeykey"
compendium_private_key = "keykeykeykey"

# server
artists_table    = "git/static/texts/artists_table.csv"
timetable_table  = "git/static/texts/timetable.csv"
images_path      = "git/static/javy/"
# local
# artists_table   = "static/texts/artists_table.csv"
# timetable_table = "static/texts/timetable.csv"
# images_path     = "static/javy/"

images_html_path = "static/javy"


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

# ################################################# MAIN  ###########################
@app.route('/')
@app.route('/home')
def main():

    try:
        infile    = open(artists_table,"r")
#
        table     = []
        headers   = []
        firstline = True
        for line in infile:
            if not firstline:
                row = line.split(";")
                table.append(row)
            else:
                row = line.split(";")
                firstline = False
                headers.append(row)
        
        return render_template('index.html', data = table)

    except Exception as e:
        return str(e) 

    
# ################################################# MAIN  ###########################

# Artists profiles
# @app.route('/', defaults={'path': ''})
@app.route('/artist/<artistname>')
def catch_all(artistname):
    artistname_space = artistname.replace('%20', ' ')
    tipo = type(artistname_space)
    artistname_space = artistname_space .decode(encoding='UTF-8',errors='strict')
    tipo = type(artistname_space)
    artistname = artistname.replace(' ', '_')
    artistname = artistname.replace('%20', '_')

    return render_template('artist.html', name = artistname, name_space = artistname_space, description = 'soon...')


# First page, before userhome
@app.route('/program')
def program():

    try:
        infile = open(artists_table,"r")
#
        table = []
        headers = []
        firstline = True
        for line in infile:
            if not firstline:
                row = line.split(";")
                table.append(row)
            else:
                row = line.split(";")
                firstline = False
                headers.append(row)


        timetable_csv = open(timetable_table,"r")
        timetable = []
        headers_timetable = []
        firstline = True
        for line in timetable_csv:
            if not firstline:
                row = line.split(";")
                timetable.append(row)
            else:
                row = line.split(";")
                firstline = False
                headers_timetable.append(row)

        return render_template('program.html', headers = headers, data = table, headers_timetable=headers_timetable, timetable=timetable)

    except Exception as e:
        return str(e) 

# About page
@app.route('/about')
def about():

    try:
        return render_template('about.html')

    except Exception as e:
        return str(e)

# Media page
@app.route('/media')
def media():

    path = images_path

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if (('.JPG')  in file) or (('.jpg')  in file) :
                 # files.append(os.path.join(r, file))
                 files.append(os.path.join(images_html_path,file))


    return render_template('media.html', images=files)


# Error handling
@app.route('/error',                methods=['GET','POST'])
def error():
    return render_template('error.html', error = 'TEST ERROR', goTo = "/")




# About page
@app.route('/test')
def test():

    try:

        path = images_path

        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if (('.JPG')  in file) or (('.jpg')  in file) :
                     files.append(os.path.join(r, file))

        print files
        print 'lalala'
        print files[0]
        return render_template('test.html', images=files, image1=files[0])

    except Exception as e:
        return str(e)

def debug(text):
  print text
  return ''


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

    app.run(host='0.0.0.0',port=5665)
