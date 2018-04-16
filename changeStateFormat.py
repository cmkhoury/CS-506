import requests
import sys
import bs4
from lxml import html
import urllib2
from faker import Faker
import sqlite3 as sql

def main():

    #Check that new user exists, then delete them
    states = [["Alabama", "AL"],
    ["Alaska", "AK"],
    ["Arizona", "AZ"],
    ["Arkansas", "AR"],
    ["California", "CA"],
    ["Colorado", "CO"],
    ["Connecticut", "CT"],
    ["Delaware", "DE"],
    ["Florida", "FL"],
    ["Georgia", "GA"],
    ["Hawaii", "HI"],
    ["Idaho", "ID"],
    ["Illinois", "IL"],
    ["Indiana", "IN"],
    ["Iowa", "IA"],
    ["Kansas", "KS"],
    ["Kentucky", "KY"],
    ["Louisiana", "LA"],
    ["Maine", "ME"],
    ["Maryland", "MD"],
    ["Massachusetts", "MA"],
    ["Michigan", "MI"],
    ["Minnesota", "MN"],
    ["Mississippi", "MS"],
    ["Missouri", "MO"],
    ["Montana", "MT"],
    ["Nebraska", "NE"],
    ["Nevada", "NV"],
    ["New Hampshire", "NH"],
    ["New Jersey", "NJ"],
    ["New Mexico", "NM"],
    ["New York", "NY"],
    ["North Carolina", "NC"],
    ["North Dakota", "ND"],
    ["Ohio", "OH"],
    ["Oklahoma", "OK"],
    ["Oregon", "OR"],
    ["Pennsylvania", "PA"],
    ["Rhode Island", "RI"],
    ["South Carolina", "SC"],
    ["South Dakota", "SD"],
    ["Tennessee", "TN"],
    ["Texas", "TX"],
    ["Utah", "UT"],
    ["Vermont", "VT"],
    ["Virginia", "VA"],
    ["Washington", "WA"],
    ["West Virginia", "WV"],
    ["Wisconsin", "WI"],
    ["Wyoming", "WY"]]

    try:
        with sql.connect("data/test.db") as con:
            curs = con.cursor()

            # states[i][0] = full Name, states[i][1] = abbreviated
            if (sys.argv[1] == "fullname"):
                for i in range(0,50):
                    query = "UPDATE User SET State=\'" + states[i][0] + "\' WHERE State = \'" + states[i][1] + "\'"
                    inserted = con.execute(query)

            else:
                for i in range(0,50):
                    query = "UPDATE User SET State=\'" + states[i][1] + "\' WHERE State = \'" + states[i][0] + "\'"
                    inserted = con.execute(query)

            con.commit()

    except Exception as e:
         con.rollback()
         print(e)

    finally:
        con.close()

if __name__ == '__main__':
    main()
