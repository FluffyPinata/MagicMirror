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
app = Flask(__name__, template_folder='template')

@app.route('/login')
def login_route():
    db = connectdb()
    #need to create login page?
    return 0;

@app.route('/createaccount')
def create_account_route():
    db = connectdb()
    #need to account creation page?
    return 0;

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

# Random generates a password of length n with letters, numbers and symbols.
def passwordgenerator(n=100):
    return ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(n))


# Creates a key which we can use to encrypt/decrypt
def makekey():
    key = Fernet.generate_key()
    return key;


# Writes a generated key to a file called key.key
def writekey():
    file = open('key.key', 'wb')
    file.write(makekey())
    file.close()


# Reads written key from key.key
def readkey():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


# First encodes a random genned password, and then encrypts with the key written to key.key
#use and store a hash of a password in the DB and compare if they match for signin
def encryptpassword():
    plength = input("How long would you like the password to be? ")
    message = passwordgenerator(int(plength)).encode()
    f = Fernet(readkey())
    encrypted = f.encrypt(message)
    return encrypted


# First decrypts the file based on the key written to key.key, then decodes to get original password.
def decryptpassword(encryptedpassword = ""):
    f = Fernet(readkey())
    decrypted = f.decrypt(encryptedpassword).decode()
    return decrypted


# Connects to the MongoDB and returns the connection.
def connectdb():
    client = MongoClient("mongodb+srv://gabriel:Citrine0407@passwordmanager-biqpk.mongodb.net/test?retryWrites=true")
    db = client.passwordobjects
    return db


# Adds a email account to the database
def addaccount(db):
    email = input("Please enter the email you have the account for: ")
    username = input("Please enter the username for the account: ")
    accountobject = {
        'email': email,
        'username': username,
        'password': encryptpassword(),
        'status': 'true'
    }
    
    # Check if user already made an account for this email
    if (db.account.find_one({'email': accountobject.get('email')})):
        print("An account for this website already exists.")
    else:
        result = db.account.insert_one(accountobject)
        print("Account successfully created.")


# Retrieves the password from the database based on email
def Signin(db):
    email = input("Please enter the email you want the password for: ")
    if (db.account.find_one({'email': email})):
        encodeddata = db.account.find_one({'email': email})
        presult = decryptpassword(encodeddata.get('password'))
        uresult = encodeddata.get('username')
        print("Your username is: " + uresult)
        print("Your password is: " + presult)
        
    else:
        print("Couldn't find an account for that website.")


def deleteaccount(db):
    email = input("Please enter the email you want to delete the account for: ")
    if (db.account.delete_one({'email': email}).deleted_count != 0):
        print("Successfully deleted account for " + email)
    else:
        print("Could not find account for " + email)


def printaccounts(db):
    print("Here are all email which have an account:")
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
            Signin(db)
            
            
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
    app.run()
    #main() #flask should be running in background