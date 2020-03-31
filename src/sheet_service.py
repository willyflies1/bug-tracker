from src.constants import CLIENT_SECRET_FILE, API_VERSION, API_SERVICE_NAME, SCOPES
import pickle
import os
from pprint import pprint as pp
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pandas as pd

cred = None

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        cred = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not cred or not cred.valid():
    if cred and cred.expired and cred.refresh_token:
        cred.refresh(Request())
else:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    cred = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(cred,token)

try:
    service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
    print('Service created successfully')
    print(service)
except Exception as e:
    print(e)
