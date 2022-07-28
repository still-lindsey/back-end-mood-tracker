import Pyrebase

firebaseConfig = {
    "API_KEY": "AIzaSyC-iJo9LmfYRITcbP8wnC2WLZFOTTmERek",
    "CLIENT_ID": "451910745718-b6e0alqb4ajc61tarnvk71v71dpej8a7.apps.googleusercontent.com",
    "REVERSED_CLIENT_ID": "com.googleusercontent.apps.451910745718-b6e0alqb4ajc61tarnvk71v71dpej8a7",
    "GCM_SENDER_ID": "451910745718",
    "PLIST_VERSION": "1",
    "BUNDLE_ID": "Lindsey.Moods",
    "PROJECT_ID": "mood-tracker-b8841",
    "STORAGE_BUCKET": "mood-tracker-b8841.appspot.com",
    "IS_ADS_ENABLED": 0,
    "IS_ANALYTICS_ENABLED": 0,
    "IS_APPINVITE_ENABLED": 1,
    "IS_GCM_ENABLED": 1,
    "IS_SIGNIN_ENABLED": 1,
    "GOOGLE_APP_ID": "1:451910745718:ios:046d6aaaef48fa323c6957",
    "DATABASE_URL": "https://mood-tracker-b8841-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth=firebase.auth()
storage=firebase.storage()

#Authentication
#Login
email = input("Enter you email")
password=input("Enter your password")
auth.sign_in_with_email_and_password(email, password)