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

        # result = urllib2.urlopen('https://fakena.me/random-real-address/').read()
        # tree = html.fromstring(result.content)
        # test_address = tree.xpath("//body/p/strong/text()")
        # print(test_address)

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
        if "Home" not in str(bucket_names): print("Logged in failed for " + users[i][0])

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
["Wyoming", "WY"]
]
        try:
            with sql.connect("data/test.db") as con:
                curs = con.cursor()
                # query = "SELECT * FROM User WHERE Username = (?)", (users[i][0],)
                for i in range(0,50):
                    query = "UPDATE User SET State=\'" + states[i][1] + "\' WHERE State = \'" + states[i][0] + "\'"
                    inserted = con.execute(query)


                # query = "UPDATE User SET State='New York' WHERE State = 'NY'"
                # inserted = con.execute( "SELECT * FROM User WHERE Username = (?)", (users[i][0],))
                # for row in inserted:
                #     if row[1] != users[i][0]:  print("Did not find " +  users[i][0])
                # deleted = con.execute("DELETE FROM User WHERE State = 'NY'")
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
