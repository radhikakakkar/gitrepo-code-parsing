import firebase_admin
from firebase_admin import credentials

SERVICE_ACCOUNT_FILE = "/Users/radhikakakkar/My\ Projects/momentum/app/config/momentum-fdc60-firebase-adminsdk-qx0o6-5e1da83d47.json"
# 'app/config/momentum-fdc60-firebase-adminsdk-qx0o6-5e1da83d47.json'

cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
firebase_admin.initialize_app(cred)
