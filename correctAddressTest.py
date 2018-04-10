import requests
import bs4
from lxml import html
from faker import Faker
import sqlite3 as sql

def main():
    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/map"

    # Generate fake users with Faker
    users = [];
    fake = Faker()
    for i in range(0, 1000):
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

        # result = urllib2.urlopen('https://fakena.me/random-real-address/').read()
        # tree = html.fromstring(result.content)
        # test_address = tree.xpath("//body/p/strong/text()")
        # print(test_address)

        try:
            result = session_requests.get("https://fakena.me/random-real-address/")
            tree = html.fromstring(result.content)
            test_address = tree.xpath("//body/div/div/p/strong/text()")
            print(test_address)
            state = test_address[1].split(",")[1].strip().split(" ")[0]
            if (state!="WI"): continue;
            print("In WI")

            city = test_address[1].split(",")[0]
            if (city!="Madison"): continue;
            print("In Madison")

            street_address = test_address[0]
            zipcode = test_address[1].split(",")[1].strip().split(" ")[1]

        except Exception as e:
            print(e)

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
        # print(payload)
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
        if "Home" in str(bucket_names): print("Logged in as " + users[i][0])
        else: print("Log in failed for " + users[i][0])

        # check if address is correctly concatenated
        test_address = "".join([street_address, ",+", city, ",+", state, ",+",  zipcode])
        result = session_requests.get("http://127.0.0.1:5000/map")
        tree = html.fromstring(result.content)
        bucket_names = tree.xpath("//script/text()")
        # print(bucket_names)
        # print(test_address)

        if(test_address in str(bucket_names)): print("Success")
        else: print("Fail")

        #Check that new user exists, then delete them
        try:
            with sql.connect("data/test.db") as con:
                curs = con.cursor()
                inserted = con.execute("SELECT * FROM User WHERE Username = (?)", (users[i][0],))
                for row in inserted:
                    if row[1] == users[i][0]:  print("Found " +  users[i][0])

                # deleted = con.execute("DELETE FROM User WHERE Username = (?)", (users[i][0],))
                # if deleted.rowcount > 0: print("Deleted " + users[i][0])
                # else: print("Delete failed")
                con.commit()

        except Exception as e:
             con.rollback()
             print(e)
        finally:
            con.close()

if __name__ == '__main__':
    main()
