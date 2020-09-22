import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:secret@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_cat(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_questions(self):
        response = self.client().get('/questions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['total_questions'], 19)

    def test_delete(self):
        response = self.client().delete('/questions/23')
        self.assertEqual(json.loads(response.data)['success'], True)

    def test_post(self):
        new_question = { 
          'question': "Test question",
          'answer': 'Testing',
          'category': 3,
          'difficulty': 3
        }

        response = self.client().post('/questions', json=new_question)
        self.assertEqual(response.status_code, 200)

    def test_post_fail(self):
        response = self.client().post('/questions', json={'test': 'fail'})
        self.assertEqual(response.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()