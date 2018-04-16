import requests
import sys
import bs4
from lxml import html
import urllib2
from faker import Faker
import sqlite3 as sql

def main():

    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/map"

    # Generate fake users with Faker
    users = [];
    fake = Faker()
    for i in range(0, int(sys.argv[1])):
        individualUser = [];
        someInfo = fake.simple_profile(sex=None) #returns simple profile  (name, email, username)
        individualUser.append(someInfo["username"])
        individualUser.append(fake.password())
        individualUser.append(someInfo["name"].split(" ")[0])
        individualUser.append(someInfo["name"].split(" ")[1])
        individualUser.append(someInfo["mail"])
        users.append(individualUser)

    for i in range(0, len(users)):
        session_requests = requests.session()

        result = session_requests.get("https://fakena.me/random-real-address/")
        tree = html.fromstring(result.content)
        test_address = tree.xpath("//body/div/div/p/strong/text()")
        # print(test_address)
        # if ("," in test_address[0]): continue;

        try:
            state = test_address[1].split(",")[1].strip().split(" ")[0]
            # if (state!="WI"): continue;
            # print("In WI")

            city = test_address[1].split(",")[0]
            # if (city != "Madison"): continue;
            # print("In Madison")

            street_address = test_address[0]
            zipcode = test_address[1].split(",")[1].strip().split(" ")[1]

        except IndexError as e:
            print("Expception: " + str(test_address))
            continue;

        # Create payload
        payload = {
            "username": users[i][0],
            "password": users[i][1],
            "firstname": users[i][2],
            "lastname": users[i][3],
            "email": users[i][4],
            "inputAddress": street_address,
            "inputCity": city,
            "inputState": state,
            "inputZip": zipcode,
        }

        print(users[i][2] + ", " + users[i][3] + ", " + users[i][0] + ", " + users[i][1])
        session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

        # Create payload to test login with new user
        payload = {
            "username": users[i][0],
            "password": users[i][1],
        }

        # Perform actual login
        result = session_requests.post("http://127.0.0.1:5000/login", data = payload, headers = dict(referer = LOGIN_URL))

        # Check if resulting page is login (failure) or home (successful)
        result = session_requests.get("http://127.0.0.1:5000/")
        tree = html.fromstring(result.content)
        bucket_names = tree.xpath("//head/comment()")
        if "Home" not in str(bucket_names): print("Logged in failed for " + users[i][0])

        # try:
        with sql.connect("data/test.db") as con:
            curs = con.cursor()
            query = "SELECT * FROM User WHERE Username = \'" + users[i][0] + "\'"
            inserted = con.execute(query)
            for row in inserted:
                if row[2] != users[i][0]:  print("Did not find " +  users[i][0])

            con.commit()

        # except Exception as e:
        #      con.rollback()
        #      print(e)
        #
        # finally:
        #     con.close()

if __name__ == '__main__':
    main()
