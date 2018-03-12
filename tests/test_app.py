import unittest

from flask import session

from app import app, database
from config import config


def login(application):
    response = application.post('/auth/testing', data=dict(
        user_id=1,
        token=1,
        first_name='Tester',
        last_name='Tester'
    ), follow_redirects=True)
    return response


def logout(application):
    response = application.get('/auth/logout', follow_redirects=True)
    return response


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config['tests'])
        self.app = app.test_client()
        database.init_db(app)
        self.assertFalse(app.debug)

    def tearDown(self):
        pass

    def test_login_and_logout(self):
        with app.test_client() as c:
            login(c)
            self.assertTrue(session.get('logged_in'))
            logout(c)
            self.assertFalse(session.get('logged_in'))

    def test_index_with_authorization(self):
        with app.test_client() as c:
            login(c)
            response = c.get('/')
            self.assertTrue(b'My polls' in response.data)
            self.assertEqual(response.status_code, 200)

    def test_index_without_authorization(self):
        with app.test_client() as c:
            response = c.get('/')
            self.assertTrue(b'Login with VK' in response.data)
            self.assertEqual(response.status_code, 200)

    def test_add_poll_with_authorization(self):
        with app.test_client() as c:
            login(c)
            response = c.post('/add_poll', data=dict(
                title='What is your favourite programing language?',
                choice=['Python', 'Ruby', 'C/C++']
            ), follow_redirects=True)
            self.assertTrue(
                b'What is your favourite programing language?' in response.data
            )
            self.assertTrue(b'Python' in response.data)
            self.assertTrue(b'Ruby' in response.data)
            self.assertTrue(b'C/C++' in response.data)
            self.assertEqual(response.status_code, 200)

    def test_add_poll_without_authorization(self):
        with app.test_client() as c:
            response = c.post('/add_poll', data=dict(
                title='What is your favourite programing language?',
                choice=['Python', 'Ruby', 'C/C++']
            ), follow_redirects=True)
            self.assertFalse(
                b'What is your favourite programing language?' in response.data
            )
            self.assertTrue(b'You are not authorized!' in response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
