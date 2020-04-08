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
# user_name = 'Hunter'
# bugs = Bug.get_bugs_by_user(user_name=user_name)
project_name = 'Example'
project_id=Bug.get_project_id(project_name=project_name)
print(project_id)
# for project in bugs.keys():
#     print('--------------------------------------------')
#     print(project)
#     print('--------------------------------------------')
#     for bug in bugs[project]:
#         print(bug)

# print by project

