import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Course, Project


def get_instructor_header():
    return get_header_for_role('INSTRUCTOR_TOKEN')


def get_program_manager_header():
    return get_header_for_role('PROGRAM_MANAGER_TOKEN')


def get_header_for_role(role):
    bearer = f'bearer {os.environ[role]}'
    return {
        "authorization": bearer
    }


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        # """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        # # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests for GET /courses
    def test_get_courses(self):
        res = self.client().get('/courses')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['courses']), 2)

    def test_404_get_courses_beyond_valid_page(self):
        res = self.client().get('/courses?page=10')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)

    # Test for POST /courses
    def test_program_manager_post_courses(self):
        body = {
            "name": "Full Stack",
            "description": "Become a Full Stack Developer with this course",
            "price": 249
        }
        headers = get_program_manager_header()
        res = self.client().post('/courses', json=body, headers=headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_403_instructor_post_courses(self):
        body = {
            "name": "Full Stack",
            "description": "Become a Full Stack Developer with this course",
            "price": 249
        }
        headers = get_instructor_header()
        res = self.client().post('/courses', json=body, headers=headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    # Test for PATCH /courses
    def test_program_manager_patch_courses(self):
        body = {
            "price": 239
        }
        headers = get_program_manager_header()
        res = self.client().patch('/courses/1', json=body, headers=headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_403_instructor_patch_courses(self):
        body = {
            "price": 239
        }
        headers = get_instructor_header()
        res = self.client().patch('/courses/1', json=body, headers=headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    # Test for DELETE /courses
    def test_program_manager_delete_courses(self):
        headers = get_program_manager_header()
        res = self.client().delete('/courses/2', headers=headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_403_instructor_delete_courses(self):
        headers = get_instructor_header()
        res = self.client().delete('/courses/2', headers=headers)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    # Test for GET /projects
    def test_get_projects(self):
        res = self.client().get('/projects')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['projects']), 2)

    def test_404_get_projects_beyond_valid_page(self):
        res = self.client().get('/projects?page=10')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 404)

    # Test for POST /projects
    def test_instructor_post_projects(self):
        body = {
            "title": "Capstone",
            "instructions": '''Build your own project using all you have
                            learned during the course''',
            "course_id": 2
        }
        headers = get_instructor_header()
        res = self.client().post('/projects', json=body, headers=headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_401_public_post_projects(self):
        body = {
            "title": "Capstone",
            "instructions": '''Build your own project using all you have
                            learned during the course''',
            "course_id": 2
        }
        res = self.client().post('/courses', json=body)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    # Test for PATCH /projects
    def test_instructor_patch_projects(self):
        body = {
            "title": "Full Stack Capstone"
        }
        headers = get_instructor_header()
        res = self.client().patch('/projects/1', json=body, headers=headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_401_public_patch_projects(self):
        body = {
            "title": "Full Stack Capstone"
        }
        res = self.client().patch('/projects/1', json=body)
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    # Test for DELETE /projects
    def test_instructor_delete_projects(self):
        headers = get_instructor_header()
        res = self.client().delete('/projects/2', headers=headers)
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_401_public_delete_projects(self):
        res = self.client().delete('/projects/2')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
