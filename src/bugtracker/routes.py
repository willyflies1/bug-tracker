from flask import Blueprint, render_template, session, request, redirect, url_for, g

# from src import User, Project, Bug
from src.api.bug import Bug
from src.api.project import Project
from src.api.user import User
from src.main.routes import load_user, make_session_permanent

bugtracker = Blueprint('bugtracker', __name__)

bugtracker.before_request(load_user)
bugtracker.before_request(make_session_permanent)


# bugtracker\routes.py
@bugtracker.route('/bug-tracker/create-project')
def create_project():
    active_window = 'create-project'
    return render_template('create-project.html', active_window=active_window)


# bugtracker\routes.py
@bugtracker.route('/bug-tracker/save-project')
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


# bugtracker\routes.py
@bugtracker.route('/bug-tracker', methods=['GET', 'POST'])
def bug_tracker():
    active_window = 'bug-tracker'

    # Possibly redundant
    user_name = g.user.screen_name

    if user_name:
        bugs = Bug.get_bugs_by_user(user_name=user_name)

    """ Pull up bugs for a project once project is submitted """
    if request.method == 'POST':
        project = request.form.get("project", None)             # Name of project selected from form
        project_bugs = bugs[project]                            # Bugs to selected project

        # Test to see if project_bugs is really what we say it is...
        # for bug in project_bugs:
        #     print('Summary: {}'.format(bug[3]))

        if project:
            return render_template('bug-tracker.html', active_window=active_window,
                                   project_bugs=project_bugs, project=project, bugs=bugs)
        pass

    return render_template('bug-tracker.html', active_window=active_window, bugs=bugs)


# bugtracker\routes.py
@bugtracker.route('/bug-tracker/new-bug')
def new_bug():
    active_window = 'new-bug'

    return render_template('new-bug.html', active_window=active_window)


# bugtracker\routes.py
@bugtracker.route('/bug-tracker/')      #http://127.0.0.1:4995/bug-tracker/new-bug?project=value&description=value
def post_bug():
    """
    Working.
    Reads in form data in the form of GET,(TODO: make this POST)
    Sends bug to database to be stored.

    :return: None
    """
    # Retrieve attributes out of http request
    project_name = request.args.get('project_name')
    description = request.args.get('description')
    issue_type = request.args.get('issue_type')
    summary = request.args.get('summary')

    # Create a Bug and save to database
    # TODO: Currently sending project_id==project_name... Needs to be changed in bug class to check for project name
    project_id=Bug.get_project_id(project_name=project_name)
    bug = Bug(project_id=project_id, description=description, issue_type=issue_type, summary=summary)
    bug.save_to_db()

    return redirect(url_for('bugtracker.bug_tracker'))


# bugtracker\routes.py
@bugtracker.route('/bug-tracker/solve-bug')
def solve_bug():
    active_window = 'solve-bug'

    if session['project_id']:
        # user = session['screen_name']

        # Get all bugs to populate select bar with project_id names for user options
        bugs = Bug.load_bugs_from_db(session['project_id'])

        return render_template('solve-bug.html', active_window=active_window, bugs=bugs)

    # Test for projec id=5 == project_name=Website
    bugs = Bug.load_bugs_from_db(5)

    return render_template('solve-bug.html', active_window=active_window, bugs=bugs)


# bugtracker\routes.py
@bugtracker.route('/bug-tracker/')      #http://127.0.0.1:4995/bug-tracker/new-bug?project=value&solution=value
def post_bug_solution():
    # Retrieve attributes out of http request
    project_name = request.args.get('project_id')
    solution = request.args.get('solution')

    # Create a Bug and save to database
    bug = Bug.load_bug_from_db(project_name)
    bug.solve_bug_on_db(solution)

    return redirect(url_for('bugtracker.bug_tracker'))