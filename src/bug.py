from src.database import CursorFromConnectionFromPool
from datetime import datetime


class Bug:

    # REQUIRES(project, description)
    def __init__(self, project, description, created_on=datetime.utcnow(), solution=None, answered_on=None, id=None):
        self.project = project
        self.description = description
        self.solution = solution if solution else None
        self.id = id
        self.created_on = created_on
        self.answered_on = answered_on if answered_on else None

    def __repr__(self):
        return "Project: {}\nDescription: {}\nCreated On: {}\n"\
            "Solution: {}\nAnswered On: {}\nId: {}".format(self.project, self.description, self.created_on,
                                                           self.solution, self.answered_on, self.id)

    def get_project(self):
        return self.project

    # Should 'set_solution' send to database? or run save_to_db after?
    def solve_bug_on_db(self, solution):
        # bug = Bug.load_bug_from_db(self.project)
        dt = datetime.utcnow()
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE bugs SET solution='{}', answered_on='{}'"
                           "WHERE id={}".format(solution, dt, self.id))

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO bugs (project, description, created_on) '
                           'VALUES (%s, %s, %s)',
                           (self.project, self.description, self.created_on))

    """
        This will retrieve the bug from the database by project.
    """

    @classmethod
    def load_bug_from_db(cls, project):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM bugs WHERE project=%s', (project,))   # expects tuple (something,<empty_field>)
            bug_data = cursor.fetchone()
            if bug_data:
                return cls(project=bug_data[1],
                           description=bug_data[2],
                           solution=bug_data[3] if bug_data[3] else None,
                           created_on=bug_data[4],
                           answered_on=bug_data[5],
                           id=bug_data[0])

    @classmethod
    def load_all_from_db(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM bugs')
            return cursor.fetchall()