# import pyrebase
import empyrebase
from dotenv import load_dotenv
import os

load_dotenv()
FB_API_KEY = os.getenv("FB_API_KEY")
FB_AUTH_DOMAIN = os.getenv("FB_AUTH_DOMAIN")
FB_PROJECT_ID = os.getenv("FB_PROJECT_ID")
FB_STORAGE_BUCKET = os.getenv("FB_STORAGE_BUCKET")
FB_MESSAGING_SENDER_ID = os.getenv("FB_MESSAGING_SENDER_ID")
FB_APP_ID = os.getenv("FB_APP_ID")
FB_MEASUREMENT_ID = os.getenv("FB_MEASUREMENT_ID")

firebaseConfig = {
  "apiKey": FB_API_KEY,
  "authDomain": FB_AUTH_DOMAIN,
  "projectId": FB_PROJECT_ID,
  "storageBucket": FB_STORAGE_BUCKET,
  "messagingSenderId": FB_MESSAGING_SENDER_ID,
  "appId": FB_APP_ID,
  "measurementId": FB_MEASUREMENT_ID,

  # Pyrebase demands a databaseUrl on initialisation
  "databaseURL": "",
}

app = empyrebase.initialize_app(firebaseConfig)

# Login Authenticator export
auth = app.auth()

# Firestore DB export
db = app.firestore()