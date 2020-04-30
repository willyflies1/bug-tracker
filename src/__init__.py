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
from flask import Flask
from src.config import Config

from src.api.database import Database

# Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")

        # Import Blueprints
        from src.main.routes import main
        from src.users.routes import users
        from src.bugtracker.routes import bugtracker
        from src.errors.handlers import errors

        # Register Blueprints
        app.register_blueprint(main)
        app.register_blueprint(users)
        app.register_blueprint(bugtracker)
        app.register_blueprint(errors)

    return app
