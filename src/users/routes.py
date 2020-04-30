from datetime import timedelta

from flask import Blueprint, session, redirect, url_for, request, render_template, current_app, g

# from src. import get_request_token, get_oauth_verifier_url, get_access_token, User
from src.api.twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from src.api.user import User

users = Blueprint('users', __name__)

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
    else:

        print('--------------------screen_name was not in session')

# Load before request
users.before_request(load_user)
users.before_request(make_session_permanent)

# users\routes.py
@users.route('/login/twitter')
def twitter_login():
    # Check to see if they are already logged in, and redirect to their profile
    if 'screen_name' in session:
        return redirect(url_for('users.profile'))

    # We need a request token 1st...
    request_token = get_request_token()
    session['request_token'] = request_token  # stores the request_token as a cookie

    # Redirect the user to Twitter so they can confirm authorization
    return redirect(get_oauth_verifier_url(request_token))

# users\routes.py
@users.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

# users\routes.py
# callback method comes here (PRETTY SURE)
@users.route('/auth/twitter')     # http://127.0.0.1:4995/auth/twitter?oauth_verifier=123456789
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

    return redirect(url_for('users.profile'))

# users\routes.py
@users.route('/profile')
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
        return redirect(url_for('users.twitter_login'))