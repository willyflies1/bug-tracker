from src.database import CursorFromConnectionFromPool
from datetime import datetime
from src.project import Project


class Bug:

    # REQUIRES(project_id, issue_type, summary, description)
    def __init__(self, project_id, issue_type, summary, description, priority=None, created_on=datetime.utcnow(),
                 solution=None, answered_on=None, id=None):
        self.project_id = project_id
        self.issue_type = issue_type
        self.summary = summary
        self.description = description
        self.priority = priority if priority else None
        self.solution = solution if solution else None
        self.id = id
        self.created_on = created_on
        self.answered_on = answered_on if answered_on else None

    def __repr__(self):
        return "Project_ID: {}\nIssue_Type: {}\nSummary: {}\nDescription: {}\nPriority: {}\nCreated On: {}\n"\
            "Solution: {}\nAnswered On: {}\nId: {}".format(self.project_id, self.issue_type, self.summary,
                                                           self.description, self.priority, self.created_on,
                                                           self.solution, self.answered_on, self.id)

    # Private to this class
    # Param: project_name
    # Return: (int) project_id
    # TODO: change bug __init__ to have project name instead of id and make this method private
    @classmethod
    def get_project_id(cls, project_name):
        project_id = Project.get_id_from_name(project_name)
        if project_id:
            return project_id

    # Returns ALL bugs created by user_name
    @classmethod
    def get_bugs_by_user(cls, user_name):
        projects = Project.get_projects_for_user(user_name=user_name)               # projects = ['p1', 'p2',...]
        project_ids = [cls.get_project_id(project) for project in projects]  # project_ids = [id=4, id=5]
        bugs = {}
        for p_id in project_ids:
            bugs[Project.get_name_from_id(p_id)] = (cls.load_bugs_with_project_id(p_id))
        return bugs


    # Should 'set_solution' send to database? or run save_to_db after?
    def solve_bug_on_db(self, solution):
        # bug = Bug.load_bug_from_db(self.project_id)
        dt = datetime.utcnow()
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE bugs SET solution='{}', answered_on='{}'"
                           "WHERE id={}".format(solution, dt, self.id))

    # TODO: Add some type of out-of-bounds for priority between 1-5
    # TODO: Currently receiving project_name from website, and trying to save as project_id (ALTER CODE)
    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO bugs (project_id, issue_type, summary, description, '
                           'priority, created_on) '
                           'VALUES (%s, %s, %s, %s, %s, %s)',
                           (self.project_id, self.issue_type, self.summary,
                            self.description, self.priority, self.created_on))

    """
        This will retrieve the bug from the database by project_id.
    """
    # TODO: Load bugs for a user.
    @classmethod
    def load_bugs_from_db(cls, project_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM bugs WHERE project_id=%s', (project_id,))   # expects tuple (something,<empty_field>)
            bug_data = cursor.fetchone()
            if bug_data:
                # project_id, issue_type, summary, description, priority, created_on=datetime.utcnow(),
                # solution=None, answered_on=None, id=None):
                return cls(project_id=bug_data[1],
                           issue_type=bug_data[2],
                           summary=bug_data[3],
                           description=bug_data[4],
                           priority=bug_data[5],
                           solution=bug_data[6] if bug_data[6] else None,
                           created_on=bug_data[7],
                           answered_on=bug_data[8],
                           id=bug_data[0])

    # TODO: Needs to grab all bugs by project_name || project_id
    @staticmethod
    def load_bugs_with_project_id(project_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM bugs WHERE project_id=%s', (project_id,))
            bugs = []
            bug_data = cursor.fetchone()
            while bug_data:
                bug = Bug(project_id=bug_data[1],
                           issue_type=bug_data[2],
                           summary=bug_data[3],
                           description=bug_data[4],
                           priority=bug_data[5],
                           solution=bug_data[6] if bug_data[6] else None,
                           created_on=bug_data[7],
                           answered_on=bug_data[8],
                           id=bug_data[0])
                # print(bug)
                # print('-------------------------------------')
                bugs.append(bug)
                bug_data = cursor.fetchone()
            return bugs
