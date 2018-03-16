from flask import Flask, render_template, request, session, send_file
import os
import sqlite3 as sql
import time
import datetime
import pdb
app = Flask(__name__)
lid = 990
global msg



@app.route('/')
def home():
      return render_template('home.html')


app.secret_key = os.urandom(12)

@app.route('/addUser')
def new_user():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # if not session.get('is_power'):
    #     return render_template('home.html')
    return render_template('addUser.html')

# CREATE TABLE User(
#     UID INTEGER PRIMARY KEY,
#     Username TEXT,
#     Password TEXT,
#     Email TEXT,
#     Address TEXT,
#     FirstName TEXT,
#     LastName TEXT,
#     OID INTEGER,


@app.route('/addUserData', methods = ['POST', 'GET'])
def addUserData():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # if not session.get('is_power'):
    #     return render_template('home.html')
    try:
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']
         aid = request.form['aid']
         firstname = request.form['firstname']
         lastname = request.form['lastname']

         with sql.connect("data/test.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO User(Username,Password,Email,Address,FirstName, LastName) VALUES (?,?,?,?,?,?)",(username,password,email,aid,firstname,lastname))
            con.commit()
            msg = "Record successfully added"
    except Exception as e:
             con.rollback()
             msg = e

    finally:
             return render_template("result.html", msg = msg)
             con.close()

if __name__ == '__main__':
    app.run(debug = True, threaded=True)