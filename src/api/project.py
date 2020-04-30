from src.api.database import CursorFromConnectionFromPool


class Project:

    # REQUIRES(user_name, project_name, private)
    def __init__(self, user_name, project_name, project_description, private, id=None):
        self.user_name = user_name
        self.project_name = project_name
        self.project_description = project_description if project_description else None
        self.private = private
        self.id = id

    def __repr__(self):
        return "ID: {}, User_name: {}, Project_name: {}\nProject_Description: {}\nPrivate: {}".format(
            self.id, self.user_name, self.project_name, self.project_description, self.private
        )

    # Adds a description to the current project
    def add_description(self, project_description):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute("UPDATE projects SET description='{}'"
                           "WHERE id={}".format(self.project_description, self.id))

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO projects (user_name, project_name, project_description, private) '
                           'VALUES (%s, %s, %s, %s)',
                           (self.user_name, self.project_name,
                            self.project_description, self.private))

    @classmethod
    def get_id_from_name(cls, project_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT id FROM projects WHERE project_name=%s', (project_name,))
            project_data = cursor.fetchone()
            if project_data:                # Only if there is a project with that name will this return anything
                return project_data[0]      # Returns an integer value (id) that matches the project name

    @classmethod
    def get_name_from_id(cls, project_id):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT project_name FROM projects WHERE id=%s', (project_id,))
            project_data = cursor.fetchone()
            if project_data:                # Only if there is a project with that name will this return anything
                return project_data[0]      # Returns an integer value (id) that matches the project name

    @classmethod
    def get_projects_for_user(cls, user_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT project_name FROM projects WHERE user_name=%s', (user_name,))
            projects = []
            project = cursor.fetchone()
            while project:
                projects.append(project[0])
                project = cursor.fetchone()
            return projects

    @classmethod
    def delete_from_db(cls, project_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('DELETE FROM projects WHERE project_name=%s',(project_name,))

    """
        This will retrieve the bug from the database by project_id.
    """
    @classmethod
    def load_project_from_db(cls, project_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM projects WHERE project_name=%s', (project_name,))   # expects tuple (something,<empty_field>)
            project_data = cursor.fetchone()
            if project_data:
                return cls(user_name=project_data[1],
                           project_name=project_data[2],
                           project_description=project_data[3] if project_data[3] else None,
                           private=project_data[4],
                           id=project_data[0])

    @classmethod
    def load_all_from_db(cls):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM projects')
            return cursor.fetchall()
