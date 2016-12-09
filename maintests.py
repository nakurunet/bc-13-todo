import unittest
import os
from flask import *
from app import *


class todoTests(unittest.TestCase):
# creates a new test client and initializes a new database
    def setUp(self):
        self.app_db, app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.list():
		
# sends HTTP GET request to the application
# to get 200 response
	def test_page_status(self):
        result = self.app.get('/') 
        self.assertEqual(result.status_code, 200) 
#test the login function	
	def test_login_set(self, username, password):
    return self.app.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)
	def test_login(self):
    logtst = self.login('Admin', 'MasterPass')
    assert 'You were logged in' in logtst.data
    logtst = self.logout()
#test the add task function		
	def test_add_task(self):
	rv = add_task()
	assertRedirects(rv, url_for('list.html'))
#test the delete tasks function		
	def test_delete_task(self):
		self.assertTrue(delete_task().task,True)
		dellist = delete_task(self)
        assertRedirects(dellist, url_for('list.html'))
#test the task resolve function		
	def test_resolve_task(self):
		resv = resolve_task()
	assertRedirects(resv, url_for('list.html'))
		
if __name__ == '__main__':
    unittest.main()