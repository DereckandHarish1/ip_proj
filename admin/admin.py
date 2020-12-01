import pyrebase

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

def check(em,pw,c):
    count=0
    for i in c:
        if i["email"] == em and i["password"] == pw:
            count=count+1
    if count>=1:
        return  True

    else:
        return False



