from flask import Flask, render_template, request, session, send_file
import os
import sqlite3 as sql
import time
import datetime
import pdb
import helper_function
app = Flask(__name__)
lid = 990
global msg

@app.route('/', methods=['POST', 'GET'])
def home():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template('home.html')
app.secret_key = os.urandom(12)

@app.route('/map')
def map():
    if not session.get('logged_in'):
       return render_template('login.html')

    con = sql.connect("data/test.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    query = "select * from User where UID=\'" + str(UID) + "\'"
    cur.execute(query)
    rows = cur.fetchall()

    if len(rows) == 0:
       return home()
    address = "".join([rows[0]['Address'], ",+",rows[0]['City'], ",+",rows[0]['State'], ",+", rows[0]['zip']])

    return render_template('geolocate.html', address = address)

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
       return render_template('login.html')

    con = sql.connect("data/test.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    query = "select * from User where UID=\'" + str(UID) + "\'"
    cur.execute(query)
    rows = cur.fetchall()

    # (Username,Password,Email,Address,City,State,Zip,FirstName,LastName)

    if len(rows) == 0:
       return home()

    profile = [];
    profile.append(rows[0]['Username'])
    profile.append(rows[0]['FirstName'])
    profile.append(rows[0]['LastName'])
    profile.append(rows[0]['Email'])
    profile.append(rows[0]['Address'])
    profile.append(rows[0]['City'])
    profile.append(rows[0]['State'])
    profile.append(rows[0]['zip'])

    return render_template('profile.html', profile = profile)


@app.route('/addUser', methods = ['POST', 'GET'])
def new_user():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # if not session.get('is_power'):
    #     return render_template('home.html')
    return render_template('addUser.html')

#CREATE TABLE User(
#  UID INTEGER PRIMARY KEY,
# Username TEXT,
#   Password TEXT,
#   Email TEXT,
#   Address TEXT,
#   Address2 TEXT,
#   City Text,
#   State Text,
#   Zip Text,
#  FirstName TEXT,
#  LastName TEXT,
#  OID INTEGER);


@app.route('/addUserData', methods = ['POST', 'GET'])
def addUserData():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    # if not session.get('is_power'):
    #     return render_template('home.html')
    try:
         username = request.form['username']
         password = helper_function.encryptPassword(request.form['password'])
         email = request.form['email']
         address = request.form['inputAddress']
         city = request.form['inputCity']
         state = request.form['inputState']
         zipActual = request.form['inputZip']
         firstname = request.form['firstname']
         lastname = request.form['lastname']

         with sql.connect("data/test.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName) VALUES (?,?,?,?,?,?,?,?,?)",
            (username,password,email,address,city,state,zipActual,firstname,lastname))
            con.commit()
            msg = "Record successfully added"
    except Exception as e:
             con.rollback()
             if (str(e) == "UNIQUE constraint failed: User.Username"):
                msg = "Username already used, go back to try another username"
             else: msg = e

    finally:
             return render_template("result.html", msg = msg)
             con.close()

@app.route('/user')
def user():

    con = sql.connect("data/test.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from User")
    rows = cur.fetchall()
    return render_template("user.html", rows = rows)

@app.route('/login', methods=['POST', 'GET'])
def login():
   global UID
   username = request.form['username']
   password = request.form['password']

   con = sql.connect("data/test.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   query = "select * from User where Username=\'" + username + "\'"
   cur.execute(query)

   rows = cur.fetchall()
   if len(rows) == 0:
      return home()
   elif helper_function.checkPassword(password.encode(), rows[0]['Password'].encode()):
      session['logged_in'] = True
      UID = rows[0]['UID']
      print("UID: ", UID)
      # if rows[0]['UserLevel'] == 'power':
      #    session['is_power'] = True
      # elif rows[0]['UserLevel'] == 'regular':
      #    session['is_regular'] = True
      return home()

   else:
      return home()

@app.route('/logout')
def logout():
   # if not session.get('logged_in'):
   #    return render_template('login.html')
   # session['is_power'] = False
   # session['is_regular'] = False
   session['logged_in'] = False
   # render_template("logout.html")
   return render_template("logout.html")

if __name__ == '__main__':
    app.run(debug = True, threaded=True)
