import os
from src.database import Database
from src.bug import Bug
import pickle
from pprint import pprint as pp
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pandas as pd
# from src.constants import CLIENT_SECRET_FILE, SCOPE, API_SERVICE_NAME, API_VERSION
# from datetime import datetime

Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")

# bug = Bug(project='Sample', description='Not a real issue...')
# bug.save_to_db()

# TEST PRINTING ALL BUGS
newBug = Bug(project='Website', description='Create a dropdown menu for the Bug Tracker App.')
newBug.save_to_db()


bugs = Bug.load_all_from_db()
for bug in bugs:
    print(bug)



# load by 'project'
print(bug)

# TEST OAUTH_GOOGLE
# cred = None
#
# if os.path.exists('token.pickle'):
#     with open('token.pickler', 'rb') as token:
#         cred = pickle.load(token)
#
# if not cred or not cred.valid:
#     if cred and cred.expired and cred.refresh_token:
#         cred.refresh(Request())
# else:
#     flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=CLIENT_SECRET_FILE, scopes=SCOPE)
#     cred = flow.run_local_server()
#
#     with open('token.pickle', 'wb') as token:
#         pickle.dump(cred, token)
#
# try:
#     service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
#     print('Service created successfully')
# except Exception as e:
#     print(e)