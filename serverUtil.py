import pymysql
import importlib
import string
import random
import configDB
import Crypto
from Crypto.Cipher import DES


def Register(username, password):
    print("Registering " + username + "...")

    db = pymysql.connect(configDB.DBaddress, configDB.DBusername, configDB.DBpassword, configDB.DBdatabase)
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES ('{0}', '{1}')".format(username, password))
    db.commit()
    cursor.close()
    db.close()

    return "valid"

def Validate(username, password):
    print("Validating user " + username + "...")

    isValid = "\nERROR - Invalid Credentials!\n"

    # Check if username exists
    db = pymysql.connect(configDB.DBaddress, configDB.DBusername, configDB.DBpassword, configDB.DBdatabase)
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = '{0}'".format(username))
    resultPassword = cursor.fetchone()
    cursor.close()
    db.close()

    if resultPassword:
        # Check if user is already logged in
        db = pymysql.connect(configDB.DBaddress, configDB.DBusername, configDB.DBpassword, configDB.DBdatabase)
        cursor = db.cursor()
        cursor.execute("SELECT status FROM users WHERE username = '{0}'".format(username))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if result[0] == "Offline":
            # Check if user's password is correct
            db = pymysql.connect(configDB.DBaddress, configDB.DBusername, configDB.DBpassword, configDB.DBdatabase)
            cursor = db.cursor()
            cursor.execute("SELECT status FROM users WHERE username = '{0}'".format(username))
            result = cursor.fetchone()
            cursor.close()
            db.close()

            if password == resultPassword[0]:
                isValid = "true"
                print("Validated.\n")
                # Set user to be Online
                db = pymysql.connect(configDB.DBaddress, configDB.DBusername, configDB.DBpassword, configDB.DBdatabase)
                cursor = db.cursor()
                cursor.execute("UPDATE users SET status = 'Online' WHERE username = '{0}'".format(username))
                cursor.close()
                db.commit()
            else:
                isValid = "\nERROR - Password is incorrect!\n"
        else:
            isValid = "\nERROR - User already logged in!\n"
    else:
        isValid = "\nERROR - Cannot find username!\n"

    return isValid
