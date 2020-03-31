import unittest
from src.bug import Bug
from src.database import Database


class ExceptionTestCase(unittest.TestCase):

    Database.initialise(database="learning", host="localhost", user="postgres", password="NightKingSusano7")

    def test_bug_init(self):
        bug = Bug('First Bug', 'This is a sample bug', 10)

        self.assertIsInstance(bug, Bug)
        self.assertEqual(bug.project, 'First Bug', msg='Title does not work.')
        self.assertEqual(bug.description, 'This is a sample bug', msg='Description is not working.')
        self.assertEqual(bug.id, 10, msg='Id not working.')

    def test_load_bug_from_db(self):
        bug = Bug.load_bug_from_db('First Bug')
        self.assertIsInstance(bug, Bug)
        self.assertEqual(bug.id, 1, msg='Incorrect ID\n\n{}'.format(bug))
