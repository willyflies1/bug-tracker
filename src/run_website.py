# Python standard libraries
import json
import os
from datetime import timedelta

# Third-party libraries
import login as login
import pytz
from flask import Flask, render_template, session, redirect, request, url_for, g
from flask_bcrypt import Bcrypt         # TODO: needs to be added to REQUIREMENTS.TXT
from flask_login import LoginManager    # TODO: needs to be added to REQUIREMENTS.TXT
import requests
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, Length, AnyOf

# Internal imports
from src.database import Database
from src.project import Project
from src.twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from src.user import User
from src.bug import Bug


"""-------------FLASK-APP-INITIALISE------------"""


# Initialise database (PostgreSQL)
# Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")



# TODO: Page to enter a new project into the database.


# app.run(port=4995, debug=True)
