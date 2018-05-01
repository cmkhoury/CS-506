'''
This file is for the helper functions.
CalculateCost
GetLocation
EncodeLocation
GetRecommendedPartners
and so on...
'''

import bcrypt
import smtplib
import sqlite3 as sql
#from flask import Flask, render_template, request, session, send_file
db = "data/test.db"

#calculate the total cost of one order/cart
def CalculateCost(base, add):
        return base+add

#calculate how much still needed for free shipping
def CalculateLeft(line, cost):
        return line-cost

#check whether the current cost reach the free shipping line
def ReachLine(line, cost):
    if(CalculateLeft(line, cost)<=0):
        return True
    return False

#encrypt the user's password for security purpose
def encryptPassword(password):
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed

#check and match the password
def checkPassword(inputPWD, hashedPWD):
    return bcrypt.checkpw(inputPWD, hashedPWD)

def sendEmail(receiver, sender):
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.login("ShippingPartnerFinder@gmail.com", "ShippingPartnerFinderPassword")
    msg = "\r\n".join(["From: "+sender,"To: "+receiver,"Subject: [CartCombo]You have a matching request!","","Hello,\n Someone want to be your shipping partner!\n You can contact with him/her by "+sender+" or check our website and merge your carts!\n"])
    s.sendmail("ShippingPartnerFinder@gmail.com", receiver, msg)
    s.quit()

def PrematchGenerator(CID1, CID2):
    con = sql.connect(db)
    con.row_factory = sql.Row
    cur = con.cursor()
    #currentUser = session.get('username')
    query = "SELECT * FROM Cart WHERE Cart.CID = \'" + str(CID1) + "\' OR Cart.CID = \'" + str(CID2) + "\'"
    cur.execute(query)
    rows = cur.fetchall()

    if(rows[0]['SID']!=rows[1]['SID']):
        msg = "Different shops can not be combined"
        print msg
    cost = CalculateCost(rows[0]['Total'], rows[1]['Total'])
    UID1_value = rows[0]['UID']
    UID2_value = rows[1]['UID']
    status = 0
    SID_value = rows[0]['SID']
    threshold = rows[0]['Threshold']

    with sql.connect(db) as con:
    	cur = con.cursor()
    	cur.execute("INSERT INTO PreMatch(UID1,UID2,Status,Cost,SID,Threshold) VALUES (?,?,?,?,?,?)",
    		(UID1_value,UID2_value,status,cost,SID_value,threshold))
    	con.commit()
    	msg = "Prematch information generated"
    	print msg
