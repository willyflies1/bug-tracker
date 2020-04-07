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


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Initialise database (PostgreSQL)
Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")

"""-----------METHODS-&-BEFORE-REQUEST------------"""


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.before_request
def load_user():
    """
    No, g is not an object to hang session data on. g data is not persisted between requests.

    session gives you a place to store data per specific browser. As a user of your Flask app,
    using a specific browser, returns for more requests, the session data is carried over
    across those requests.

    g on the other hand is data shared between different parts of your code base within one request
    cycle. g can be set up during before_request hooks, is still available during the
    teardown_request phase and once the request is done and sent out to the client, g is cleared.
    """
    print('load_user()-----------------------------')
    print('if screen_name in session:')
    if 'screen_name' in session:
        print('screen_name: {}, is in session'.format(session['screen_name']))
        g.user = User.load_db_by_screen_name(session['screen_name'])
        print('g.user.screen_name: {}'.format(g.user.screen_name))
    print('--------------------screen_name was not in session')


def date_time_filter(value, format="%m/%d/%y"):
    tz = pytz.timezone('US/Eastern') # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)


app.jinja_env.filters['datetimefilter'] = date_time_filter


"""-----------------WEB-PAGES-------------------"""


@app.route('/home')
@app.route('/')
def home():
    active_window = 'home'

    return render_template('index.html', active_window=active_window)





@app.route('/login/twitter')
def twitter_login():
    # Check to see if they are already logged in, and redirect to their profile
    if 'screen_name' in session:
        return redirect(url_for('profile'))
        print('screen_name is in session. Should go to profile')

    # We need a request token 1st...
    request_token = get_request_token()
    session['request_token'] = request_token  # stores the request_token as a cookie

    # Redirect the user to Twitter so they can confirm authorization
    return redirect(get_oauth_verifier_url(request_token))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# callback method comes here (PRETTY SURE)
@app.route('/auth/twitter')     # http://127.0.0.1:4995/auth/twitter?oauth_verifier=123456789
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    # access_token cannot be used more than once
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], id=None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    active_window = 'profile'
    """
        If you have logged in previously, then you will be directed to profile.html
        If you are not currently logged in, you are directed to twitter_login
    """
    if 'screen_name' in session:
        user = User.load_db_by_screen_name(session['screen_name'])
        return render_template('profile.html', user=user, active_window=active_window)
    else:
        return redirect(url_for('twitter_login'))


@app.route('/bug-tracker/create-project')
def create_project():
    active_window = 'create-project'
    return render_template('create-project.html', active_window=active_window)


@app.route('/bug-tracker/save-project')
def save_project():
    # user = g.user
    # session_user = session['screen_name']
    user = User.load_db_by_screen_name(session['screen_name'])
    active_window = 'bug-tracker'
    project_name = request.args.get('project_name')
    private = True if request.args.get('private')=='private' else False
    description = request.args.get('description')

    # print("session_user: {}\nproject_name: {}\n"
    #       "private: {}\ndescription: {}".format(user_name, project_name,
    #                                             private, description))
    project = Project(user_name=user.screen_name, project_name=project_name,
                      private=private, project_description=description)

    # project.save_to_db()

    return render_template('bug-tracker.html', active_window=active_window)

@app.route('/bug-tracker')
def bug_tracker():
    active_window = 'bug-tracker'

    # TODO: possibly use WTF forms to display form. If user has projects -> display projects and bugs
    # TODO: If user does not have projects -> "Would you like to add a project?"
    """
    <div class="row">
              <div class="col-md-1">{{ bug[0] }}</div>
              <div class="col-md-1">{{ project }}</div>
              <div class="col-md-4">{{ bug[4] }}</div>
              <div class="col-md-4">{{ bug[6] }}</div>
              <div class="col-md-1">{{ bug[7] | datetimefilter }}</div>
              <div class="col-md-1">{{ bug[8] | datetimefilter if bug[8] else bug[8] }}</div>
            </div>
    
    """

    user_name = g.user.screen_name
    if user_name:
        bugs = Bug.get_bugs_by_user(user_name=user_name)
    # bugs = Bug.load_bug_from_db()

    return render_template('bug-tracker.html', active_window=active_window, bugs=bugs)


@app.route('/bug-tracker/new-bug')
def new_bug():
    active_window = 'new-bug'

    return render_template('new-bug.html', active_window=active_window)


@app.route('/bug-tracker/')      #http://127.0.0.1:4995/bug-tracker/new-bug?project=value&description=value
def post_bug():
    # Retrieve attributes out of http request
    project_name = request.args.get('project_name')
    description = request.args.get('description')
    issue_type = request.args.get('issue_type')
    summary = request.args.get('summary')

    # Create a Bug and save to database
    # TODO: Currently sending project_id=project_name... Needs to be changed in bug class to check for project name
    project_id=Bug.get_project_id(project_name=project_name)
    bug = Bug(project_id=project_id, description=description, issue_type=issue_type, summary=summary)
    bug.save_to_db()

    return redirect(url_for('bug_tracker'))


@app.route('/bug-tracker/solve-bug')
def solve_bug():
    active_window = 'solve-bug'

    # Get all bugs to populate select bar with project_id names for user options
    bugs = Bug.load_all_from_db()

    return render_template('solve-bug.html', active_window=active_window, bugs=bugs)


@app.route('/bug-tracker/')      #http://127.0.0.1:4995/bug-tracker/new-bug?project=value&solution=value
def post_bug_solution():
    # Retrieve attributes out of http request
    project_name = request.args.get('project_id')
    solution = request.args.get('solution')

    # Create a Bug and save to database
    bug = Bug.load_bug_from_db(project_name)
    bug.solve_bug_on_db(solution)

    return redirect(url_for('bug_tracker'))


@app.route('/search')       # http://127.0.0.1:4995/search?q=cars+filter:images
def search():
    query = request.args.get('q')

    # computers+filter:images
    tweets = g.user.user_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label
    return render_template('search.html', content=tweet_texts)

# TODO: Page to enter a new project into the database.


app.run(port=4995, debug=True)
