import os
from src.database import Database
from src.bug import Bug
from src.project import Project

Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")

# ADD NEW BUGS
# bug = Bug(project_id=4, issue_type='Bug', summary='Database Functionality',
#           description='Now can it successfully submit with a priority?',
#           priority=3)
# bug.save_to_db()

# projects = Project.get_projects_for_user('Hunter')
# print(projects)
bugs = Bug.get_bugs_by_user('Hunter')
print(bugs['Website'])
# print(Bug.load_bugs_by_project_from_db(4))

# Project.delete_from_db('example')
