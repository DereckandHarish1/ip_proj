import pyrebase
import re
from validate_email import validate_email
from werkzeug.security import check_password_hash
config = {
    "apiKey": "AIzaSyBX9wuQLsiRvzY0cOWgsbyEyN3SYQ2G9L8",
    "authDomain": "admin-c96e0.firebaseapp.com",
    "databaseURL": "https://admin-c96e0.firebaseio.com",
    "projectId": "admin-c96e0",
    "storageBucket": "admin-c96e0.appspot.com",
    "messagingSenderId": "688616953815",
    "appId": "1:688616953815:web:61a13072f93189fbf75d92",
    "measurementId": "G-QD865HKN6G"
}


def store(value):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("Details").push({"Details": value})


def store_feedback(value):
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("Feedback").push({"Details": value})


def ret_feedback():
    b = []
    c = []
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    Details = db.child("Details").get().val()
    for key, value in Details.items():
        b.append(value)
    for i in b:
        for x in i.values():
            c.append(x)
    return c




def ret():
    b = []
    c = []
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    Details = db.child("Details").get().val()
    for key, value in Details.items():
        b.append(value)
    for i in b:
        for x in i.values():
            c.append(x)
    return c


def check(em, pw, c):
    count = 0
    for i in c:
        if i["email"] == em and i["password"] == pw:
            count = count + 1
    if count >= 1:
        return True

    else:
        return False


# a = ret()

def email_check(em, c1):
    c = 0
    for i in c1:
        if i["email"] == em:
            c = c + 1
    if c > 0:
        return False
    else:
        return True


# b = ret()
# a = unique("dereckjos12@gmail.com", b)

def email_valid(text):
    # s = text
    # match = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', s, re.I)
    is_valid = validate_email(email_address=text, check_regex=True, check_mx=True,
                              smtp_timeout=10, dns_timeout=10, use_blacklist=True, debug=False)

    return is_valid


def pass_check(t1, t2):
    if t1 == t2:
        return True
    else:
        return False


def ret_pass(email):
    b = []
    c = []
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    Details = db.child("Details").get().val()
    for key, value in Details.items():
        b.append(value)
    for i in b:
        for x in i.values():
            c.append(x)
    for i in c:
        if i["email"]==email:
            return i["password"]


def email_pass(email,pas):
    passs = ret_pass(email)


def check2(em, pw, c):
    count = 0
    for i in c:
        if i["email"] == em and check_password_hash(i["password"],pw):
            count = count + 1
    if count >= 1:
        return True

    else:
        return False

