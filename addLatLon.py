import requests
import bs4
from lxml import html
import urllib2
from faker import Faker
import sqlite3 as sql
import json
import ast

def main():

    # try:
        with sql.connect("data/test.db") as con:
            curs = con.cursor()
            session_requests = requests.session()

            query = "SELECT * FROM User WHERE UID > 733"
            missingLatLon = con.execute(query)
            for row in missingLatLon:
                # 1, None, ckhoury, password, ckhoury@wisc.ed, 44 Clay Street, Yonkers, New York, 10701, Cam, Khoury, None, None, None)
                address = "".join([str(row[5]), ",+", str(row[6]), ",+", str(row[7]), ",+", str(row[8])])
                # print(address)
                apiKEY = "AIzaSyBRx7Cu0K1yT5nS9qZFiSbRaQZpPxz_9wk"
                call = "".join(["https://maps.googleapis.com/maps/api/geocode/json?address=", address, "&key=", apiKEY])
                # print(call)
                response = requests.get(call)
                json_data = response.json()

                # If google can't get a lat lon from the address, it's one of the fake ones
                if (json_data['status'] == "ZERO_RESULTS"):
                    print("Fake Address Found")
                    continue;

                lat = str(json_data['results'][0]['geometry']['location']['lat'])
                lon = str(json_data['results'][0]['geometry']['location']['lng'])
                print(lat + ", " + lon)

                query2 = "UPDATE User SET Lat=\'" + lat + "\', Lon=\'" + lon + "\' WHERE UID = \'" + str(row[0]) + "\'"
                updated = con.execute( query2 )

                checkUpdate = con.execute( "SELECT * FROM User WHERE UID=\'" + str(row[0]) + "\'")
                for new in checkUpdate:
                    if (str(new[11]) != lat) or (str(new[12]) != lon): print("Lat / Lon Mismatch between geocoded value and value in database")

            con.commit()

                # print("Found " +  str(row[0]))

            # deleted = con.execute("DELETE FROM User WHERE UID = (?)", (93,))
            # print("Deleted: " + str(deleted.rowcount) + " entries.")


    # except Exception as e:
    #      con.rollback()
    #      print(e)

    # finally:
    #     con.close()

if __name__ == '__main__':
    main()
