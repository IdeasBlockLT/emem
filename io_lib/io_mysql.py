# -*- coding: utf-8 -*-
from    __future__      import unicode_literals
import  io_debug
import  MySQLdb as mysql
import  os
import  io_credentials

IO_DEBUG = 0
# These environnment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME    = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER               = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD           = os.environ.get('CLOUDSQL_PASSWORD')

# MySQL configurations
db_username       = io_credentials.db_username
db_password       = io_credentials.db_password
db_dbname         = io_credentials.db_dbname
hostname          = io_credentials.hostname
tablename         = io_credentials.tablename

# ==========================    SQL     =============================
class io_mysql:
    io_print = None
    conn     = None


    def __init__(self, io_print, io_log, print_All):
        if print_All:
            self.io_print = io_debug.io_debug(io_print, io_log).io_print
        else:
            self.io_print = io_debug.io_debug(False, io_log).io_print
        return


    def configure_credentials(self, username, password, database):
        db_username = username
        db_password = password
        db_dbname   = database

        return

    def connect(self):
        try:
            self.conn = mysql.connect(
                host        = '127.0.0.1',
                user        = db_username,
                passwd      = db_password,
                db          = db_dbname,
                use_unicode = True,
                charset     = 'utf8')
            self.io_print('\tConnected: '+str(self.conn)+'\n')
            return True
        except mysql.Error as err:
            self.io_print("Something went wrong: {}".format(err))
            raise

    def disconnect(self):
        try:
            if self.conn != None:
                self.conn.close()
                self.io_print("\tDisconnected: mysql database...\n")
                return
            raise Exception('No first connection created.')
        except (mysql.Error, Exception) as err:
            self.io_print('\t'+str(err))
            # We don't want to raise an exception here because calling this method and failing means,
            # that something went wrong on main and it was not able to reach a connect, this may be a
            # waterfall of errors, raising this may clutter the caller.
            #raise

    def execute(self, query, commit=False):
        # Execute can work in two ways:
        # 1) When we want to request data to mysql we use "commit" parameter as False.
        # 2) When we want to write data to mysql we use "commit" parameter as True.
        # return empty array of data if an error happened.
        try:
            cursor = self.conn.cursor()
            self.io_print('\t'+query)
            cursor.execute(query)
            if commit:
                data = self.conn.commit()
            else:
                data = cursor.fetchall()
            self.io_print('\tSuccessfull query: ' + str(data))
            cursor.close()
            return data
        except mysql.Error as err:
            self.io_print('\t[x]Something went wrong: {}'.format(err))
            raise



    def general_search(self, query, queryString):
        try:
            cursor = self.conn.cursor()

            cursor.execute(query, {
                'query': queryString
            })

            data = cursor.fetchall()

            self.io_print('\tSuccessfull query: ' + str(data))

            cursor.close()
            return data

        except mysql.Error as err:
            self.io_print('\t[x]Something went wrong: {}'.format(err))
            raise


    def sp_create_user(self, name, email, password,description, latitude, longitude, city, picture):

        try:

            cursor = self.conn.cursor()
            query = "SELECT * FROM user_info WHERE facebook_name = %(user_name)s;"
            cursor.execute(query, {
                'user_name': name
            })

            data = cursor.fetchall()


            if len(data) > 0:
                return 'User already registered'

            self.io_print('\tSuccessfull query: ' + str(data))

            cursor.close()

            cursor = self.conn.cursor()
            query = ("INSERT "
                "INTO user_info (user_name, facebook_name, user_email, user_password, description, latitude, longitude, city, profile_picture)"
                "VALUES(%(user_name)s, %(facebook_name)s, %(user_email)s, %(user_password)s, %(description)s, %(latitude)s, %(longitude)s, %(city)s, %(profile_picture)s)"
                )

            cursor.execute(query, {
                'user_name': name, 
                'facebook_name': name, 
                'user_email': email, 
                'user_password': password, 
                'description': description, 
                'latitude': latitude, 
                'longitude': longitude, 
                'city': city,
                'profile_picture':picture
            }) 
            # print cursor
            # cursor.callproc('sp_create_user_compendium',(name,email,password, description, latitude, longitude))
            data = self.conn.commit()
            
            cursor.close()
            return True
            # if len(data) == 0:
            #     self.io_print("Commit to DB")
            #     self.conn.commit()
            #     cursor.close()
            #     return True
            # else:
            #     self.io_print("error committing to DB")
            #     cursor.close()
            #     return False
        except mysql.Error as err:
            self.io_print("Something went wrong: {}".format(err))
            raise


# ==========================    SQL     =============================
