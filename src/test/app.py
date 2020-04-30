from src.api.database import Database
from src.api.bug import Bug

Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")

# ADD NEW BUGS
# bug = Bug(project_id=4, issue_type='Bug', summary='Database Functionality',
#           description='Now can it successfully submit with a priority?',
#           priority=3)
# bug.save_to_db()

# projects = Project.get_projects_for_user('Hunter')
# print(projects)
user_name = 'files_hunter'
bugs = Bug.get_bugs_by_user(user_name=user_name)
project_name = 'Example'
project_id=Bug.get_project_id(project_name=project_name)
print(project_id)
# for project in bugs.keys():
#     print('--------------------------------------------')
#     print(project)
#     print('--------------------------------------------')
#     for bug in bugs[project]:
#         print(bug)

project = 'Example'
project_bugs = bugs[project]
for bug in project_bugs:
    print('Created on: {}'.format(bug.created_on))
    # print(bug)
# print by project


