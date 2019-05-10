"""
Basic webapp.
Registery / Login pages
Html, Bootstrap for frontend
Python Flask and Sqlite for backend
contains 8 pages, registery / Login system are just normal html
"""
from flask import Flask, render_template, url_for, request
import sqlite3 as sq
import time, os

#-- Database section using Sqlite for data handling
#-- Create function creates a connection file if doesn't exists
def create():
    db = sq.connect("site_db")
    cursor = db.cursor()
    print("creating database connection file!")
    time.sleep(1)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password BLOB) """)
    db.commit()

#-- Insert function add new record to database
def insert(name, email, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""INSERT INTO users (name, email, password) VALUES(?,?,?)""",(name,email,password))
    db.commit()
    db.close()

#-- basic data check, using email address to check if user already registred or not
def check_data(email):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE email=(?)""",(email,))
    data = cursor.fetchall()
    if len(data) == 0:
        return True
#-- Basic data check, using email and password to check if user entred correct login info
def check_login_data(email, password):
    db = sq.connect("site_db")
    cursor = db.cursor()
    cursor.execute("""SELECT email FROM users WHERE email=(?)""",(email,))
    data = cursor.fetchall()
    print(data)
    if len(data) > 0:
        cursor.execute("""SELECT password FROM users WHERE password=(?)""",(password,))
        data = cursor.fetchall()
        print(data)
        if len(data) > 0:
            return True

#-- calling the create function each time
create()

#-- Create an object from Flask class basically app is the core of our backend
app = Flask(__name__)

#-- mapping for home page(root)
#-- using decorator function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

#-- mapping for about page
@app.route("/about")
def about():
    return render_template("about.html")

#-- mapping for register page
@app.route("/register")
def register():
    return render_template("register.html")

#-- mapping for register_success page
#-- the registery page uses post method to send data to server
@app.route("/register_success", methods = ["POST", "GET"])
def register_success():
    #-- checking for method and runing data check before sending data to
    #-- Sqlite
    if request.method == "POST":
        email = request.form["email"]
        if check_data(email):
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            print(name)
            print(email)
            print(password)
            insert(name, email, password)
            return render_template("register_success.html")
        else:
            return render_template("register_fail.html")

#-- Registery fail page
@app.route("/register_faile")
def register_faile():
    return render_template("register_faile.html")
#-- Login page
@app.route("/login")
def login():
    return render_template("login.html")

#-- same as register_success page here we use POST method to send data
#-- back to server, so we can run data check for login proccess
@app.route("/login_success", methods = ["POST", "GET"])
def login_success():
    #-- using email and password
    #-- first check if even email exists if yes checks for password
    #-- we can expand system by creating auto send reset link to user Email
    #-- in a case that they forgot their password
    if request.method == "POST":
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        print(password)
        if check_login_data(email, password):
            return render_template("login_success.html")
        else:
            return render_template("login_fail.html")


if __name__ == "__main__":
    #-- run the app in debug mode
    app.run(debug = True)
