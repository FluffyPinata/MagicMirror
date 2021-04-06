#mongo cluster info: https://cloud.mongodb.com/v2/5cbf6a95cf09a2b538fb0bb3#metrics/replicaSet/600de9d9a6646f6c0026b348/explorer/passwordobjects/account/find
#using nodejs and flask to communicate information
import hashlib
import string
import secrets
import os
import json
import cryptography
import flask
from flask_socketio import SocketIO
from flask import Flask, render_template, request
from flask import flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from pymongo import MongoClient
from pprint import pprint
import urllib
from urllib.request import urlopen
import ast
import socket
import requests
#for getting user location
from contextlib import closing

from flask import Flask, render_template 
 
app = Flask(__name__) 
 
@app.route('/') 
def content(): 
	with open("logininfo.txt", 'r') as f: 
		return render_template("content.html", text=f.read()) 
      
def print_to_file(username, location, status):
    f = open("logininfo.txt", "w")
    f.write(str(username) + "\n" + str(location) + "\n" + str(status) + "\n")
    f.close()
    return 0

def hashpassword():
    #change this to input password
    password = input("What would you like your password to be?")
    encrypted = hash(password)
    return encrypted

def p_hashpassword(password):
    encrypted = hash(password)
    return encrypted

def getlocation():
    fqn = socket.getfqdn()
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}
    url = 'https://ident.me'
    request = urllib.request.Request(url,None,headers) #The assembled request
    ext_ip = urlopen(request).read().decode("utf8")
    print ("Asset: %s " % fqn, "Checking in from IP#: %s " % ext_ip)
    url = 'http://ip-api.com/json/' + ext_ip
    req = urllib.request.Request(url)
    out = urllib.request.urlopen(req).read().decode("utf8")
    #Country/State/City
    dict_out = ast.literal_eval(out)
    country = dict_out['country']
    state = dict_out['regionName']
    city = dict_out['city']
    location_dict = {'country': country, 'state': state, 'city': city}
    return location_dict

# Connects to the MongoDB and returns the connection.
def connectdb():
    client = MongoClient("mongodb+srv://gabriel:Citrine0407@passwordmanager-biqpk.mongodb.net/test?retryWrites=true")
    db = client.passwordobjects
    return db


# Adds a email account to the database
def addaccount(db):
    #add one way hash and compare passwords
    #add location to this later
    email = input("Please enter the email you have the account for: ")
    username = input("Please enter the username for the account: ")
    password = input("Please enter the password for the account: ")
    var = password.encode('ascii')
    hashed_password = hashlib.sha224(var).hexdigest()
    answer_location = input("Would you like us to use your location for convenience and other applications?")
    if (answer_location == "yes"):
        location = getlocation()
    else:
        location = {'country': 'null', 'state': 'null', 'city': 'null'}
    accountobject = {
        'email': email,
        'username': username,
        'password': hashed_password,
        'location': location,
        'status': 'true'
    }
    
    # Check if user already made an account for this email
    if (db.account.find_one({'email': accountobject.get('email')})):
        print("An account for this website already exists.")
    else:
        db.account.insert_one(accountobject)
        print("Account successfully created.")
        
# Answer location is yes if getting location allowed, anything else will result in not gettin it
def p_addaccount(db, email, username, password, answer_location):
    
    var = password.encode('ascii')
    hashed_password = hashlib.sha224(var).hexdigest()
    
    if (answer_location == "yes"):
        location = getlocation()
    else:
        location = {'country': 'null', 'state': 'null', 'city': 'null'}
        accountobject = {
            'email': email,
            'username': username,
            'password': hashed_password,
            'location': location,
            'status': 'true'
        }
    
    # Check if user already made an account for this email
    if (db.account.find_one({'email': accountobject.get('email')})):
        print("An account for this website already exists.")
    else:
        db.account.insert_one(accountobject)
        print("Account successfully created.")


# Retrieves the password from the database based on email
def signin(db):
    #upload login details in file to flask after successful login
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    var = password.encode('ascii')
    hashed_password = hashlib.sha224(var).hexdigest()
    if (db.account.find_one({'username': username})):
        account_info = db.account.find_one({'username': username})
        account_phash = account_info.get('password')
        account_location = account_info.get('location')
        account_status = account_info.get('status')
        if (account_phash == hashed_password):
            print_to_file(username, account_location, account_status)
            print("Passwords match, successfully logged in")
            return True
        else:
            print("Login failed, passwords don't match")
            return False
        
    else:
        print("Couldn't find an account with that username")
        return False
        
def p_signin(db, username, password):
    #upload login details in file to flask after successful login

    #hashed_password = hash(password)
    var = password.encode('ascii')
    hashed_password = hashlib.sha224(var).hexdigest()
    print(hashed_password)

    if (db.account.find_one({'username': username})):
        account_info = db.account.find_one({'username': username})
        account_phash = account_info.get('password')
        account_location = account_info.get('location')
        account_status = account_info.get('status')
        print("username entered is:" + username)
        print("password entered is:" + password)
        if (account_phash == hashed_password):
            print_to_file(username, account_location, account_status)
            print("Passwords match, successfully logged in")
            return True
        else:
            print("Login failed, passwords don't match")
            return False
        
    else:
        print("Couldn't find an account with that username")
        return False



def deleteaccount(db):
    email = input("Please enter the email you want to delete the account for: ")
    if (db.account.delete_one({'email': email}).deleted_count != 0):
        print("Successfully deleted account for " + email)
    else:
        print("Could not find account for " + email)
        
def p_deleteaccount(db, email):
    if (db.account.delete_one({'email': email}).deleted_count != 0):
        print("Successfully deleted account for " + email)
    else:
        print("Could not find account for " + email)


def printaccounts(db):
    print("Here are all emails which have an account:")
    listaccounts = db.account.find()
    for i in listaccounts:
        print(i.get('email'))

def main():
    db = connectdb()
    print("-------------------------------------------")
    print("Manager supports the following commands:")
    print("Signup - adds an account using a email, a username, and a randomly generated password.")
    print("Signin - will retrieve the password from the database for usage.")
    print("Deleteaccount - will delete a saved account from the database.")
    print("quit - quits application.")  #will just be a button eventually so can get rid of
    print("-------------------------------------------")
    while (1):
        choice = input("$: ")
        if (choice == "signup"):
            created = addaccount(db)
            if created:
                print("account created\n")

        elif (choice == "signin"): #just need to return true 
            signedIn = signin(db)
            
            
            #flask server is on localhost:5000
            #use fetch command in JS
            
            
            if signedIn:
                print("signed in successfully\n")
                #os.system('npm start')
            app.run()
            r = requests.post("http://localhost:5000/", data={'number': 12524, 'type': 'issue', 'action': 'show'})
            print(r.status_code, r.reason)
            
        elif (choice == "deleteaccount"):
            deleteaccount(db)
        elif (choice == "printaccounts"): #don't need
            printaccounts(db)
        elif (choice == "quit"):
            return
        else:
            print("Bad choice, please try again.")


if __name__ == '__main__':
    #app.run()
    main() #flask should be running in background