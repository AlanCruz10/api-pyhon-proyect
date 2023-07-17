import firebase_admin
from firebase_admin import credentials


def firebase():
    cred = credentials.Certificate('./configurations/configuration_firebase.json')
    initialize_app = firebase_admin.initialize_app(cred,
                                                   {'databaseURL': 'https://amili-7cf9e-default-rtdb.firebaseio.com/'})
    return initialize_app
