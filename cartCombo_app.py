from flask import Flask, render_template, request, session, send_file
import os
import sqlite3 as sql
import time
import datetime
import pdb
import helper_function
import json
import requests
import re
import time
from lxml import html


app = Flask(__name__)
lid = 990
global msg
db = "data/test.db"

@app.route('/', methods=['POST', 'GET'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    if session.get('is_power'):
        return render_template('powerHome.html')
    else:
        return render_template('home.html')
       #if session.get('is_regular'):
        #   return render_template('home.html')
       #if session.get('is_power'):
        #   return render_template('powerHome.html')

app.secret_key = os.urandom(12)

@app.route('/api/updateUser', methods=['POST', 'GET'])
def updateUser():
    adrParts = [None] * 4;
    if not session.get('logged_in'):
       return render_template('login.html')
    try:
        with sql.connect("data/test.db") as con:

            # (Username,Password,Email,Address,City,State,Zip,FirstName,LastName)
            addressFormatted = ""
            curs = con.cursor()
            con = sql.connect(db)
            con.row_factory = sql.Row
            username = session.get('username')

            args = request.args
            keys = args.keys()
            values = args.values()
            print("got here")
            for i in range(0, len(values)):
                print(keys[i] + values[i])
                #Need to update Lat Lon in the database if address changes
                #In addition, seems like parts of address do not arrive in order they are sent? Address is sometimes last in for loop.  Put the different parts of the address in in boxes of array to keep them in order
                if keys[i]=="address": adrParts[0] = values[i]
                elif keys[i]=="city": adrParts[1] = values[i]
                elif keys[i]=="state": adrParts[2] = values[i]
                elif keys[i]=="zip": adrParts[3] = values[i]

                query = "UPDATE User SET " + keys[i] + "=\'" + str(values[i]) + "\' WHERE Username = \'" + username + "\'"
                inserted = con.execute(query)

            print(adrParts[0])

            if adrParts[0] is not None:
                for i in range(0, len(adrParts)):
                    addressFormatted = "".join([addressFormatted, adrParts[i]])
                    if (i != len(adrParts)-1): addressFormatted = "".join([addressFormatted, ",+"])

                apiKEY = "AIzaSyBRx7Cu0K1yT5nS9qZFiSbRaQZpPxz_9wk"
                call = "".join(["https://maps.googleapis.com/maps/api/geocode/json?address=", addressFormatted, "&key=", apiKEY])
                response = requests.get(call)
                json_data = response.json()

                lat = str(json_data['results'][0]['geometry']['location']['lat'])
                lon = str(json_data['results'][0]['geometry']['location']['lng'])
                print(lat + ", " + lon)

                query = "UPDATE User SET Lat=\'" + str(lat) + "\' WHERE Username = \'" + username + "\'"
                con.execute(query)
                query = "UPDATE User SET Lon=\'" + str(lon) + "\' WHERE Username = \'" + username + "\'"
                con.execute(query)

            con.commit()
            return "success"

    except Exception as e:
         con.rollback()
         print(e)
         return "error"

    finally:
        con.close()
        return "FINALLY"



@app.route('/map')
def map():
    if not session.get('logged_in'):
       return render_template('login.html')

    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    query = "SELECT * FROM User WHERE UID=\'" + str(UID) + "\'"
    cur.execute(query)
    rows = cur.fetchall()

    if len(rows) == 0:
       return home()

    return render_template('browse.html', lat = rows[0]['Lat'], lon = rows[0]['Lon'], state = rows[0]['State'], uid = rows[0]['UID'])

@app.route('/api/nearbyShoppers')
def nearbyShoppers():
    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    state = request.args.get('state');
    uid = request.args.get('uid');
    query1 = "SELECT * FROM User WHERE State = \'" + str(state) + "\'"
    query2 = "SELECT * FROM User WHERE UID = \'" + str(uid) + "\'"

    cur.execute(query1 + " EXCEPT " + query2)
    rows = cur.fetchall()
    results = list()
    for x in range(0, len(rows)):
        user = dict()
        user["username"] = rows[x]['Username'];
        user["firstname"] = rows[x]['FirstName'];
        user["lastname"] = rows[x]['LastName'];
        user["email"] = rows[x]['Email'];
        user['streetaddress'] = rows[x]['Address']
        user["city"] = rows[x]['City'];
        user["state"] = rows[x]['State'];
        user["zip"] = rows[x]['Zip'];
        user["lat"] = rows[x]['Lat'];
        user["lon"] = rows[x]['Lon'];
        user['uid'] = rows[x]['UID'];
        results.append(user)

    return json.dumps(results)

@app.route('/api/createMatch')
def createMatch():
    otherID = request.args.get('otherID');

	# `PMID`	INTEGER,
	# `UID1`	INTEGER,
	# `UID2`	INTEGER,
	# `STATUS1`	BOOLEAN,
	# `STATUS2`	BOOLEAN,
	# `Cost`	NUMERIC,
	# `Threshold`	NUMERIC,
	# `SID`	INTEGER,
	# FOREIGN KEY(`UID2`) REFERENCES `User`(`UID`),
	# FOREIGN KEY(`UID1`) REFERENCES `User`(`UID`),
	# PRIMARY KEY(`PMID`)

    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    uid = request.args.get('uid');
    query1 = "SELECT * FROM PreMatch WHERE (UID1 = " + str(UID) + " AND UID2 = " + str(otherID) + ") OR (UID1 = " + str(otherID) + " AND UID2 = " + str(UID) + ")"

    cur.execute(query1)
    rows = cur.fetchall()
    results = list()

    if len(rows) > 0: return "Match already exists"

    query2 = "INSERT INTO PreMatch (UID1, UID2, STATUS1, STATUS2, Cost, Threshold) VALUES (" + str(UID) + ", " + str(otherID) + ", 1, 0, 0, 0 )"
    cur.execute(query2)
    con.commit();
    # //write an email with http://127.0.0.1:5000/acceptMatch?uid1=&&uid2=

    # sender = "ShippingPartnerFinder@gmail.com"
    # query3 = "SELECT Email FROM User WHERE UID = \'" + str(otherID) + "\'"
    # cur.execute(query3)
    # receiver = cur.fetchall()[0][0]
    #
    # s = smtplib.SMTP('smtp.gmail.com',587)
    # s.ehlo()
    # s.starttls()
    # s.login("ShippingPartnerFinder@gmail.com", "ShippingPartnerFinderPassword")
    # msg = "\r\n".join(["From: "+sender,"To: "+receiver,"Subject: [CartCombo]You have a matching request!","","Hello,\n Someone want to be your shipping partner!\n You can contact with him/her by "+sender+" or check our website and merge your carts!\n"])
    # s.sendmail("ShippingPartnerFinder@gmail.com", receiver, msg)
    # s.quit()
    return "success"

@app.route('/api/determineStatus')
def determineStatus():
    otherID = request.args.get('otherID');

	# `PMID`	INTEGER,
	# `UID1`	INTEGER,
	# `UID2`	INTEGER,
	# `STATUS1`	BOOLEAN,
	# `STATUS2`	BOOLEAN,
	# `Cost`	NUMERIC,
	# `Threshold`	NUMERIC,
	# `SID`	INTEGER,
	# FOREIGN KEY(`UID2`) REFERENCES `User`(`UID`),
	# FOREIGN KEY(`UID1`) REFERENCES `User`(`UID`),
	# PRIMARY KEY(`PMID`)

    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    uid = request.args.get('otherID');
    query1 = "SELECT * FROM PreMatch WHERE (UID1 = " + str(UID) + " AND UID2 = " + str(otherID) + ") OR (UID1 = " + str(otherID) + " AND UID2 = " + str(UID) + ")"

    cur.execute(query1)
    rows = cur.fetchall()
    if len(rows) < 1 : return otherID
    result = []
    for x in range(0, len(rows)):
        pair = dict()
        pair["uid1"] = rows[x]['UID1'];
        pair["uid2"] = rows[x]['UID2'];
        pair["status1"] = rows[x]['status1'];
        pair["status2"] = rows[x]['status2'];
        result.append(pair)
    return json.dumps(result);


@app.route('/acceptMatch')
def acceptMatch():
    # if not session.get('logged_in'):
    #     return render_template('login.html')

    UID = request.args.get('uid1'); #logged in user
    otherID = request.args.get('uid2');

    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    uid = request.args.get('uid');
    query1 = "SELECT * FROM PreMatch WHERE (UID1 = " + str(UID) + " AND UID2 = " + str(otherID) + ") OR (UID1 = " + str(otherID) + " AND UID2 = " + str(UID) + ")"

    cur.execute(query1)
    rows = cur.fetchall()
    results = list()

    if len(rows) > 0:
                        # cur.execute("UPDATE Item SET DESCRIPTION = '" + description + "', SID = 'AMAZON', PRICE = '" + price + "' WHERE DESCRIPTION = '" + description + "'")
        query2 = "UPDATE PreMatch SET STATUS2 = 1 WHERE (UID1 = " + str(UID) + " AND UID2 = " + str(otherID) + ") OR (UID1 = " + str(otherID) + " AND UID2 = " + str(UID) + ")"
        cur.execute(query2)
        con.commit();
        # query3 = "UPDATE PreMatch   WHERE (UID1 = " + str(UID) + " AND UID2 = " + str(otherID) + ") OR (UID1 = " + str(otherID) + " AND UID2 = " + str(UID) + ")"
        return "match succesful: UID: " + UID + " UID2: " + otherID + " both accepted"


@app.route('/profile')
def profile():
    if not session.get('logged_in'):
       return render_template('login.html')

    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from User where UID=\'" + str(UID) + "\'")
    rows = cur.fetchall()

    # (Username,Password,Email,Address,City,State,Zip,FirstName,LastName)

    if len(rows) == 0:
       return home()

    profile = dict();
    profile['username']= rows[0]['Username']
    profile['uid'] = rows[0]['UID']
    profile['firstname']= rows[0]['FirstName']
    profile['lastname'] = rows[0]['LastName']
    profile['email'] = rows[0]['Email']
    profile['address'] = rows[0]['Address']
    profile['city'] = rows[0]['City']
    profile['state'] = rows[0]['State']
    profile['zip'] = rows[0]['zip']

    query = "SELECT Cart.CID AS 'CartID',Cart.Total AS 'Total',Item.Description AS 'Description',Item.IID AS 'ItemID',Item.Price AS 'Price', Item.Quantity AS 'Quantity' FROM Cart INNER JOIN CartItem ON Cart.CID = CartItem.CID INNER JOIN Item ON CartItem.IID = Item.IID WHERE UID = \'" + str(UID) + "\'"
    cur.execute(query)
    rows = cur.fetchall()

    listOfCarts = [];
    listofItems = [];
    unRatedUsers = [];

    for x in range(0, len(rows)):
      cart = dict()
      cart['cartID'] = rows[x]['CartID']
      cart['total'] = rows[x]['total']
      if(cart not in listOfCarts): listOfCarts.append(cart)
      item = dict()
      item['cartID'] = rows[x]['CartID']
      item['itemID'] = rows[x]['ItemID']
      item['price'] = rows[x]['Price']
      item['description'] = rows[x]['Description']
      item['quantity'] = rows[x]['Quantity']
      if(item not in listofItems): listofItems.append(item)

    number = 10;
    query = "SELECT * FROM User WHERE UID < \'" + str(number) + "\'"
    cur.execute(query)
    rows = cur.fetchall()

    for x in range(0, len(rows)):
        user = []
        user.append(rows[x]['Username'])
        user.append(rows[x]['FirstName'])
        user.append(rows[x]['LastName'])
        user.append(rows[x]['UID'])
        unRatedUsers.append(user)

    return render_template('profile.html', profile = profile, unRatedUsers = unRatedUsers)


@app.route('/addUser', methods = ['POST', 'GET'])
def new_user():
    # if not session.get('logged_in'):
    #     return render_template('login.html')

    return render_template('addUser.html')

@app.route('/wishlist', methods = ['POST', 'GET'])
def wishlist():
    # if not session.get('logged_in'):
    #     return render_template('login.html')
    id = request.args.get("id")
    session_requests = requests.session()
    result = session_requests.get("http://www.justinscarpetti.com/projects/amazon-wish-lister/api/?id=" + str(id))

    if(len(result.json()) == 0):
        for x in range (0,3):
            result = session_requests.get("http://www.justinscarpetti.com/projects/amazon-wish-lister/api/?id=" + str(id))
            time.sleep(.5)

    # tree = html.fromstring(result.content)
    # $(.*?)\$
    #print(str(result.json()[0]['new-price']))


    with sql.connect(db) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Cart (UID) VALUES ('" + str(UID) + "')")
        #cur.commit()
        cur.execute("SELECT last_insert_rowid()")
        cartID = cur.fetchall()[0][0]
        print(cartID)

        for x in range(0,len(result.json())):
            description = str(result.json()[x]['name'])
            tempPrice = re.search(r"\$(.*?)\<", str(result.json()[x]['new-price']), 0)
            price = tempPrice.groups()[0]
            #print(description)
            cur.execute("SELECT DESCRIPTION, IID FROM Item WHERE DESCRIPTION = '" + description +"'")
            results = cur.fetchall()

            if (len(results) == 0):
                cur.execute("INSERT INTO Item (DESCRIPTION, SID, PRICE) VALUES ('" + description + "', 'AMAZON', '" + price + "')")
                con.commit()
                cur.execute("SELECT last_insert_rowid()")
                itemID = cur.fetchall()[0][0]
                print(itemID)
            else:
                itemID = results[0][1]
                cur.execute("UPDATE Item SET DESCRIPTION = '" + description + "', SID = 'AMAZON', PRICE = '" + price + "' WHERE DESCRIPTION = '" + description + "'")
                con.commit()
                print(itemID)

            cur.execute("INSERT INTO CartItem(CID, IID) VALUES ('" + str(cartID) + "', '"+ str(itemID) +"')")
    con.close()


    # http://www.justinscarpetti.com/projects/amazon-wish-lister/api/?id=3SE72T48T8WG6
     # response = requests.get(call)
    #print(result.json())

    return str(result.json())

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

         addressFormatted = "".join([address, ",+", city, ",+", state, ",+", zipActual])
         apiKEY = "AIzaSyBRx7Cu0K1yT5nS9qZFiSbRaQZpPxz_9wk"
         call = "".join(["https://maps.googleapis.com/maps/api/geocode/json?address=", addressFormatted, "&key=", apiKEY])
         # print(call)
         response = requests.get(call)
         json_data = response.json()

        # # If google can't get a lat lon from the address, it's one of the fake ones
        #  if (json_data['status'] == "ZERO_RESULTS"):
        #      print("Fake Address Found")
        #      continue;

         lat = str(json_data['results'][0]['geometry']['location']['lat'])
         lon = str(json_data['results'][0]['geometry']['location']['lng'])

         with sql.connect(db) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO User(Username,Password,Email,Address,City,State,Zip,FirstName,LastName,Lat,Lon) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (username,password,email,address,city,state,zipActual,firstname,lastname,lat,lon))
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

    con = sql.connect(db)
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from User")
    rows = cur.fetchall()
    return render_template("user.html", rows = rows)

@app.route('/carts')
def carts():

    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    currentUser = session.get('username')
    query = "SELECT * FROM Cart INNER JOIN User ON Cart.UID=User.UID WHERE Username = \'" + currentUser + "\'"
    cur.execute(query)
    rows = cur.fetchall()
    return render_template("carts.html", rows = rows)

@app.route('/login', methods=['POST', 'GET'])
def login():
   global UID
   username = request.form['username']
   print(username)
   password = request.form['password']
   print(password)
   con = sql.connect(db)
   con.row_factory = sql.Row
   cur = con.cursor()

   query = "SELECT * FROM User WHERE Username=\'" + username + "\'"
   cur.execute(query)
   rows = cur.fetchall()

   if len(rows) == 0:
      return home()

   elif helper_function.checkPassword(password.encode(), rows[0]['Password'].encode()):
       if rows[0]['UserLevel'] == 'power':
          session['is_power'] = True
       elif rows[0]['UserLevel'] == '':
          session['is_regular'] = True
       session['logged_in'] = True
       session['username'] = username
       UID = rows[0]['UID']
      #print("UID: ", UID)

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

@app.route('/searchPartner')
def searchPartner():
  return render_template("searchPartner.html")

@app.route('/api/searchPartner') #?name = "XXX"
def searchPartner_api():

  con = sql.connect(db)
  con.row_factory = sql.Row
  cur = con.cursor()
  name = request.args.get('name');
  query = "select * from User WHERE Username LIKE \'%" + str(name) + "%\' OR FirstName LIKE \'%" + str(name) + "%\' OR LastName LIKE \'%" + str(name) + "%\'"
  cur.execute(query)
  rows = cur.fetchall()
  results = list()
  for x in range(0, len(rows)):
    user = dict()
    user["email"] = rows[x]['email'];
    user["username"] = rows[x]['username'];
    user["address"] = rows[x]['address'];
    user["city"] = rows[x]['city'];
    user["state"] = rows[x]['state'];
    user["zip"] = rows[x]['zip'];
    user["firstname"] = rows[x]['firstname'];
    user["lastname"] = rows[x]['lastname'];
    results.append(user)


  #if len(rows) == 0:

  return json.dumps(results);

@app.route('/api/searchCart')
def searchCart_api():
  con = sql.connect(db)
  con.row_factory = sql.Row
  cur = con.cursor()

  query = "SELECT Cart.CID AS 'CartID',Cart.Total AS 'Total',Item.Description AS 'Description',Item.IID AS 'ItemID',Item.Price AS 'Price', Item.Quantity AS 'Quantity' FROM Cart INNER JOIN CartItem ON Cart.CID = CartItem.CID INNER JOIN Item ON CartItem.IID = Item.IID WHERE UID = \'" + str(UID) + "\'"
  cur.execute(query)
  rows = cur.fetchall()

  listOfCarts = [];
  listofItems = [];

  for x in range(0, len(rows)):
    cart = dict()
    cart['cartID'] = rows[x]['CartID']
    cart['total'] = rows[x]['total']
    if(cart not in listOfCarts): listOfCarts.append(cart)
    item = dict()
    item['cartID'] = rows[x]['CartID']
    item['itemID'] = rows[x]['ItemID']
    item['price'] = rows[x]['Price']
    item['description'] = rows[x]['Description']
    item['quantity'] = rows[x]['Quantity']
    if(item not in listofItems): listofItems.append(item)

  results = [listOfCarts, listofItems]
  return json.dumps(results)


@app.route('/api/hasUsername') #?username = "XXX"
def hasUsername_api():
  con = sql.connect(db)
  con.row_factory = sql.Row
  cur = con.cursor()
  name = request.args.get('username');
  query = "select * from User WHERE Username = \'"+ str(name) + "\'"
  cur.execute(query)
  rows = cur.fetchall()
  return json.dumps(len(rows) != 0);

if __name__ == '__main__':
    app.run(debug = True, threaded=True)
