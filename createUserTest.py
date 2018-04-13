import requests
import bs4
from lxml import html
import urllib2
from faker import Faker
import sqlite3 as sql

def main():

    LOGIN_URL = "http://127.0.0.1:5000/addUserData"
    URL = "http://127.0.0.1:5000/addUserData"
    users = [
        ['snehausername', 'hello', 'Sneha', 'Patri', 'sneha@wisc.edu', '210 N Charter St Apt 203', 'Madison', 'Wisconsin', '53715'],
        ['geeth', 'hello', 'Geeth', 'Anand', 'geeth@wisc.edu', '1423 Monroe Street Apt 306', 'Madison', 'Wisconsin', '53711'],
        ['wilson', 'hello', 'Wilson', 'Brown', 'wilson@wisc.edu', '1402 Regent Street Apt 504', 'Madison', 'Wisconsin', '53711'],
        ['jeff_1', 'hello', 'Jeff', 'Yang', 'jeff@wisc.edu', '1022 West Johnson Street Apt 214', 'Madison', 'Wisconsin', '53715'],
        ['dan', 'hello', 'Dan', 'Luther', 'dan@wisc.edu', '1650 Kronshage Drive, Dormitory 314', 'Madison', 'Wisconsin', '53706'],
        ['sam', 'hello', 'Sam', 'Parker', 'sam@wisc.edu', '1415 Engineering Drive', 'Madison', 'Wisconsin', '53706'],
        ['matt', 'hello', 'matt', 'Leblanc', 'wilson@wisc.edu', '437 N Francis St', 'Madison', 'Wisconsin', '53711'],
        ['gpicc', 'hello', 'Greg', 'Piccirillo', 'wilson@wisc.edu', '165 Kronshage Dr', 'Madison', 'Wisconsin', '53706'],
        ['jeff_2', 'hello', 'Tyler', 'Waite', 'wilson@wisc.edu', '535 W Johnson St', 'Madison', 'Wisconsin', '53711'],
        ['aguo', 'hello', 'Alina', 'Guo', 'wilson@wisc.edu', '535 W Johnson St', 'Madison', 'Wisconsin', '53711'],
        ['martin', 'hello', 'Martin', 'Skreli', 'wilson@wisc.edu', '202 N Brooks St', 'Madison', 'Wisconsin', '53715'],
        ['briankh', 'hello', 'Brian', 'Khoury', 'wilson@wisc.edu', '4829 Sheboygan Avenue', 'Madison', 'Wisconsin', '53705'],
        ['marilynpicc', 'hello', 'Marilyn', 'Piccirillo', 'mpiccirillo@wisc.edu', '1001 University Avenue', 'Madison', 'Wisconsin', '53715'],
        ['harrisonguo', 'hello', 'Harrison', 'Guo', 'mpiccirillo@wisc.edu', '777 University Avenue', 'Madison', 'Wisconsin', '53715'],
        ['jjuennamann', 'hello', 'John', 'Juennamann', 'john@wisc.edu', '716 Langdon St', 'Madison', 'Wisconsin', '53715'],
        ['clucke', 'hello', 'Charlie', 'Lucke', 'clucke@wisc.edu', '2 Gerry Ct', 'Madison', 'Wisconsin', '53715'],
        ['bblanke', 'hello', 'Becky', 'Blanke', 'bblanke@wisc.edu', '1323 W Dayton St', 'Madison', 'Wisconsin', '53715'],
    ]

    # Generate fake users with Faker
    # fake = Faker()
    # for i in range(0, 1):
    #     individualUser = [];
    #     someInfo = fake.simple_profile(sex=None) #returns simple profile  (name, email, username)
    #     individualUser.append(someInfo["username"])
    #     individualUser.append(fake.password())
    #     individualUser.append(someInfo["name"].split(" ")[0])
    #     individualUser.append(someInfo["name"].split(" ")[1])
    #     individualUser.append(someInfo["mail"])
    #     individualUser.append(fake.street_address())
    #     individualUser.append(fake.city())
    #     individualUser.append(fake.state())
    #     individualUser.append(fake.postcode())
    #     users.append(individualUser)

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
