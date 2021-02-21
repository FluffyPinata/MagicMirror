#mongo cluster info: https://cloud.mongodb.com/v2/5cbf6a95cf09a2b538fb0bb3#metrics/replicaSet/600de9d9a6646f6c0026b348/explorer/passwordobjects/account/find
#using nodejs and flask to communicate information
import string
import secrets
import os
import json
import cryptography
import flask
from flask_socketio import SocketIO
from flask import Flask, render_template, request
from cryptography.fernet import Fernet
from pymongo import MongoClient
from pprint import pprint
import urllib
from urllib.request import urlopen
import socket
#for getting user location
from contextlib import closing
app = Flask(__name__, template_folder='template')

@app.route('/upload') #return a json obj
def upload_file():
   return render_template('index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      #f = request.files['file']
      #f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
#****************************************************************************

def hashpassword():
    #change this to input password
    password = input("What would you like your password to be?")
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
    return out

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
    hashed_password = hashpassword()
    location = getlocation()
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
    hashed_password = hash(password)
    if (db.account.find_one({'username': username})):
        account_info = db.account.find_one({'username': username})
        account_phash = account_info.get('password')
        if (account_phash == hashed_password):
            print("Passwords match, successfully logged in")
        else:
            print("Login failed, passwords don't match")
        
    else:
        print("Couldn't find an account with that username")


def deleteaccount(db):
    email = input("Please enter the email you want to delete the account for: ")
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
    print("Addaccount - adds an account using a email, a username, and a randomly generated password.")
    print("Signin - will retrieve the password from the database for usage.")
    print("Deleteaccount - will delete a saved account from the database.")
    print("quit - quits application.")  #will just be a button eventually so can get rid of
    print("-------------------------------------------")
    while (1):
        choice = input("$: ")
        if (choice == "addaccount"):
            addaccount(db)
        elif (choice == "Signin"): #just need to return true 
            signin(db)
            
            
            #flask server is on localhost:5000
            #use fetch command in JS
            
            
            #if usernames match
                #os.system('npm start')
            
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