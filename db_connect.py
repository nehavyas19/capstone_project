#Connect to mysql database
# Only for the loan app data analysis requirement, getting the connection as global variable

import mysql.connector
from mysql.connector import errorcode
from config import db

#Get DB user/pwd
db_user = db.get('DATABASE_USER')
db_pass = db.get('DATABASE_PASSWORD')
db_name = 'creditcard_capstone'
global mysql_connect

try:
    mysql_connect = mysql.connector.connect(host='localhost', user=db_user, password=db_pass, database=db_name)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)