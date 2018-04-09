import requests
import bs4
from lxml import html

def main():
    LOGIN_URL = "http://127.0.0.1:5000/login"
    URL = "http://127.0.0.1:5000/"

    usernames = ["hello", "wrong", 'wrong', "wrong", "maybe?", "hello"]
    passwords = ["", "no", "i even k", "kay", "", ""]
    fails = 0
    passes = 0

    for i in range(0, len(usernames)):
        session_requests = requests.session()

        # Create payload
        payload = {
            "username": usernames[i],
            "password": passwords[i],
        }

        # Perform login
        result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

        # Scrape url
        result = session_requests.get(URL)
        tree = html.fromstring(result.content)
        bucket_names = tree.xpath("//head/comment()")
        if ("Home" in str(bucket_names[0])):
            passes += 1
            print("Destination: Home page (login successful)")
        else:
            fails +=1
            print("Destination: Login page (login rejected)")

    if (passes == 2 and fails == 4):
        print("TEST PASSED (6/6 login attempts correct)")
    else:
        print("TEST FAILED")

if __name__ == '__main__':
    main()
