""""
/app
├── /application
│   ├── __init__.py
│   ├── auth.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── /static
│   │   ├── /dist
│   │   └── /src
│   └── /templates
├── config.py
├── start.sh
└── wsgi.py
"""

# # Python standard libraries
# import json
# import os
#
# # Third-party libraries
# import login as login
# import pytz
# from flask import Flask, render_template, session, redirect, request, url_for, g
# from flask_bcrypt import Bcrypt         # TODO: needs to be added to REQUIREMENTS.TXT
# from flask_login import LoginManager    # TODO: needs to be added to REQUIREMENTS.TXT
# import requests
# from flask_wtf import Form
# from wtforms import StringField
# from wtforms.validators import InputRequired, Length, AnyOf
#
# # Internal imports
# from src.database import Database
# from src.project import Project
# from src.twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
# from src.user import User
# from src.bug import Bug
#
#
# def create_app():
#
#     app = Flask(__name__)
#     # app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
#     app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or os.urandom(24)
#
#     Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")
#
#     """----------IMPORT-BLUEPRINTS-----------"""
#
#     from src.main import main as main_blueprint
#     app.register_blueprint(main_blueprint, url_prefix="")
#
#     from src.auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint, url_prefix="")
#
#     return app

"""----https://hackersandslackers.com/flask-application-factory-----"""
# # Python standard libraries
# import json
import os
#
# # Third-party libraries
# import login as login
# import pytz
from flask import Flask, render_template, session, redirect, request, url_for, g
# from flask_bcrypt import Bcrypt         # TODO: needs to be added to REQUIREMENTS.TXT
# from flask_login import LoginManager    # TODO: needs to be added to REQUIREMENTS.TXT
# import requests
# from flask_wtf import Form
# from wtforms import StringField
# from wtforms.validators import InputRequired, Length, AnyOf
#
# # Internal imports
from src.database import Database
from src.project import Project
from src.twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from src.user import User
from src.bug import Bug


def create_app():
    """Initialize the core application"""
    app = Flask(__name__, )