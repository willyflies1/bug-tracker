from datetime import timedelta

import pytz
import requests
from flask import Blueprint, session, current_app, render_template, request, g

from src.api.user import User

main = Blueprint('main', __name__)

"""-----------METHODS-&-BEFORE-REQUEST------------"""


# @main.before_request
def make_session_permanent():
    session.permanent = True

    # app => current_app ???
    current_app.permanent_session_lifetime = timedelta(minutes=5)

# @main.before_request
def load_user():
    print('load_user()-----------------------------')
    print('if screen_name in session:')
    if 'screen_name' in session:
        print('screen_name: {}, is in session'.format(session['screen_name']))
        g.user = User.load_db_by_screen_name(session['screen_name'])
        print('g.user.screen_name: {}'.format(g.user.screen_name))

    print('--------------------screen_name was not in session')

main.before_request(make_session_permanent)
main.before_request(load_user)

def date_time_filter(value, format="%m/%d/%y"):
    tz = pytz.timezone('US/Eastern') # timezone you want to convert to from UTC
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)


current_app.jinja_env.filters['datetimefilter'] = date_time_filter


"""-----------------WEB-PAGES-------------------"""


# main\routes.py
@main.route('/home')
@main.route('/')
def home():
    active_window = 'home'

    return render_template('index.html', active_window=active_window)


# (deprecated) main\routes.py
@main.route('/search')       # http://127.0.0.1:4995/search?q=cars+filter:images
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