import requests
import bs4
from lxml import html
import urllib2
from faker import Faker
import sqlite3 as sql

def main():

    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/addUserData"

    # Generate fake users with Faker
    users = [];
    fake = Faker()
    for i in range(0, 1):
        individualUser = [];
        someInfo = fake.simple_profile(sex=None) #returns simple profile  (name, email, username)
        individualUser.append(someInfo["username"])
        individualUser.append(fake.password())
        individualUser.append(someInfo["name"].split(" ")[0])
        individualUser.append(someInfo["name"].split(" ")[1])
        individualUser.append(someInfo["mail"])
        individualUser.append(fake.street_address())
        individualUser.append(fake.city())
        individualUser.append(fake.state())
        individualUser.append(fake.postcode())
        users.append(individualUser)

    for i in range(0, len(users)):
        session_requests = requests.session()

        # Create payload
        payload = {
            "username": users[i][0],
            "password": users[i][1],
            "firstname": users[i][2],
            "lastname": users[i][3],
            "email": users[i][4],
            "inputAddress": users[i][5],
            "inputCity": users[i][6],
            "inputState": users[i][7],
            "inputZip": users[i][8]
        }
        print(users[i][2] + ", " + users[i][3] + ", " + users[i][0] + ", " + users[i][1])
        # Add user
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
        if "Home" in str(bucket_names): print("Logged in as " + users[i][0])
        else: print("Log in failed for " + users[i][0])

        #Check that new user exists, then delete them
        try:
            with sql.connect("data/test.db") as con:
                curs = con.cursor()
                inserted = con.execute("SELECT * FROM User WHERE Username = (?)", (users[i][0],))
                for row in inserted:
                    if row[1] == users[i][0]:  print("Found " +  users[i][0])

                deleted = con.execute("DELETE FROM User WHERE Username = (?)", (users[i][0],))
                if deleted.rowcount > 0: print("Deleted " + users[i][0])
                else: print("Delete failed")
                con.commit()

        except Exception as e:
             con.rollback()
             print(e)
        finally:
            con.close()

if __name__ == '__main__':
    main()
