import requests
import sys
import bs4
from lxml import html
import urllib2
from faker import Faker
import sqlite3 as sql

session_requests = requests.session()

def check(exp, msgfail, msgsucceed):
    if(not exp):
        # if msgfail is not None:
        print("     check failed: " + msgfail);
        print("     ********TEST FAILED********")
        sys.exit()
    elif msgsucceed is not None:
        print("     " +  msgsucceed);

def main():
    users = [];
    fake = Faker()
    individualUser = [];

    for i in range(0, 10):
        someInfo = fake.simple_profile(sex=None) #returns simple profile  (name, email, username)
        individualUser.append(someInfo["username"])
        individualUser.append(fake.password())
        individualUser.append(someInfo["name"].split(" ")[0])
        individualUser.append(someInfo["name"].split(" ")[1])
        individualUser.append(someInfo["mail"])

        result = session_requests.get("https://fakena.me/random-real-address/")
        tree = html.fromstring(result.content)
        test_address = tree.xpath("//body/div/div/p/strong/text()")
        # print(test_address)
        # if ("," in test_address[0]): continue;

        try:
            individualUser.append(test_address[0]) #street address
            individualUser.append(test_address[1].split(",")[0]) #city
            individualUser.append(test_address[1].split(",")[1].strip().split(" ")[0]) #state
            individualUser.append(test_address[1].split(",")[1].strip().split(" ")[1]) #zip
            users.append(individualUser)
            break;

        except IndexError as e:
            print("Expception when creating user: " + str(test_address))
            continue;

    addUser(users)
    correctAddress(users)
    correctProfile(users)
    deleteUser(users)


def addUser(users):
    states = [
    ["Alabama", "AL"],
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

    print("\nStarting addUser test: ")
    # print(users)
    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/map"
    # session_requests = requests.session()
    # Generate fake users with Faker

    # Create payload
    payload = {
        "username": users[0][0],
        "password": users[0][1],
        "firstname": users[0][2],
        "lastname": users[0][3],
        "email": users[0][4],
        "inputAddress": users[0][5],
        "inputCity": users[0][6],
        "inputState": users[0][7],
        "inputZip": users[0][8],
    }

    # print(users[0][2] + ", " + users[0][3] + ", " + users[0][0] + ", " + users[0][1])
    session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Create payload to test login with new user
    payload = {
        "username": users[0][0],
        "password": users[0][1],
    }

    # Perform actual login
    result = session_requests.post("http://127.0.0.1:5000/login", data = payload, headers = dict(referer = LOGIN_URL))

    # Check if resulting page is login (failure) or home (successful)
    result = session_requests.get("http://127.0.0.1:5000/")
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//head/comment()")
    check("Home" in str(bucket_names),
        "Log in failed for " + users[0][0] + ".",
        users[0][0] + ": Succesful log in.")

    try:
        with sql.connect("data/test.db") as con:
            curs = con.cursor()
            query = "SELECT * FROM User WHERE Username = \'" + users[0][0] + "\'"
            inserted = con.execute(query)
            for row in inserted:
                check(row[2] == users[0][0],
                    users[0][0] + " not found in database.",
                    users[0][0] + ": Found in database.")
                # print(row[3],row[4],row[5],row[6], row[7],row[8])
                check("@" in row[4], users[0][0] + ": no @ in email address.",None)

                userStateCorrect = False;
                for state in states:
                    if row[7]==state[1]:
                        userStateCorrect = True;
                        break;

                check(userStateCorrect, users[0][0] + ": US State format incorrect or not present.", users[0][0] + ": US State formatted correctly.")

            con.commit()

    except Exception as e:
         con.rollback()
         print(e)

    finally:
        con.close()

    print("     TEST PASSED")

def deleteUser(users):
    print("\nStarting deleteUser test: ")

    try:
        with sql.connect("data/test.db") as con:
            curs = con.cursor()
            query = "SELECT * FROM User WHERE Username = \'" + users[0][0] + "\'"
            inserted = con.execute(query)
            inserted = inserted.fetchall()
            check(len(inserted) != 0, users[0][0] + ": Not found in database, can't delete.", None)

            for row in inserted:
                check(row[2] == users[0][0], None, users[0][0] + ": Found in database, deleting.")

            con.execute("DELETE FROM User WHERE Username = \'" + users[0][0] + "\'")

            inserted = con.execute(query)
            for row in inserted:
                check(row[2] != users[0][0], users[0][0] + ": Still found in database.", None)

            con.commit()

    except Exception as e:
         con.rollback()
         print(e)

    finally:
        con.close()

    print("     TEST PASSED")

def correctAddress(users):
    print("\nStarting correctAddress test: ")

    # Create payload to test login with new user
    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/map"

    payload = {
        "username": users[0][0],
        "password": users[0][1],
    }

    # Perform actual login
    result = session_requests.post("http://127.0.0.1:5000/login", data = payload, headers = dict(referer = LOGIN_URL))

    # Check if resulting page is login (failure) or home (successful)
    result = session_requests.get("http://127.0.0.1:5000/")
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//head/comment()")
    check("Home" in str(bucket_names),
        "Log in failed for " + users[0][0] + ".",
        users[0][0] + ": Succesful log in.")

    # check if address is correctly concatenated
    test_address = "".join([users[0][5], ",+", users[0][6], ",+", users[0][7], ",+",  users[0][8]])
    result = session_requests.get("http://127.0.0.1:5000/map")
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//script/text()")

    streetaddress = users[0][7]
    first400char = bucket_names[0][:400]

    check(streetaddress in first400char, users[0][0] + ": Address in map is incorrect.",
            users[0][0] + ": Correct street address in map.")

    print("     TEST PASSED")

def correctProfile(users):
    print("\nStarting correctProfile test: ")

    # Create payload to test login with new user
    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/profile"

    payload = {
        "username": users[0][0],
        "password": users[0][1],
    }

    # Perform actual login
    result = session_requests.post("http://127.0.0.1:5000/login", data = payload, headers = dict(referer = LOGIN_URL))

    # Check if resulting page is login (failure) or home (successful)
    result = session_requests.get("http://127.0.0.1:5000/")
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//head/comment()")
    check("Home" in str(bucket_names), "Log in failed for " + users[0][0] + ".",
        users[0][0] + ": Succesful log in.")

    result = session_requests.get("http://127.0.0.1:5000/profile")
    tree = html.fromstring(result.content)

    profileFirstName = tree.xpath("//span[contains(@id,'firstname_p')]/text()")[0]
    check(profileFirstName == users[0][2], users[0][0] + ": First name on profile page incorrect.",
        users[0][0] + ": Correct first name profile page.")

    profileLastName = tree.xpath("//span[contains(@id,'lastname_p')]/text()")[0]
    check(profileLastName == users[0][3], users[0][0] + ": Last name on profile page incorrect.",
        users[0][0] + ": Correct last name profile page.")



    print("     TEST PASSED")

if __name__ == '__main__':
    main()
