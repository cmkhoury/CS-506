import unittest
from unittest import TestCase
import sys
sys.path.append("..")
import cartCombo_app
#from flask_testing import TestCase
import flask
import urllib2
from flask import session
import tempfile

class test_cartCombo_app(TestCase):

    def setUp(self):
        cartCombo_app.db = '../data/test2.db'
        #cartCombo_app.
        cartCombo_app.app.config['TESTING'] = True
        #cartCombo_app.app.config['SECRET_KEY'] = 'sekrit'
        #cartCombo_app.app.config['LIVESERVER_PORT'] = 5000
        #cartCombo_app.app.config['LIVESERVER_TIMEOUT'] = 10
        self.app = cartCombo_app.app.test_client()

    def tearDown(self):
        cartCombo_app.db = '/data/test.db'

    def login(self, username, password):
        return self.app.post('/login', data = {
            'username' : username,
            'password' : password
        }, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', 
            data = {}, 
            follow_redirects = True)

    ''' test functions '''

    def test_single_valid_login(self):
        '''in test_single_valid_login'''
        rv = self.login('hello', '')
        #print "in test_single_valid_login"
        #print rv.data
        self.assertIn("This is the Home Page", rv.data)

    def test_single_valid_login_single_logout(self):
        rv = self.login('hello','')
        rv = self.logout()
        #print "in test_single_valid_login_single_logout"
        #print rv.data
        self.assertIn("You've been successfully logged out", rv.data)
        

    def test_invalid_login_home(self):
        #print "in test_invalid_login_home"
        rv = self.login('hello','')
        #print rv.data
        rv = self.logout()
        #print rv.data
        rv = self.app.get('/')
        #print rv.data
        self.assertIn("This is the Login Page", rv.data)



    '''def test_home_login(self):
        with self.app.test_client().session_transaction() as sess:
            sess['logged_in'] = True
            self.app.test_client().get('/')
            self.assert_template_used('home.html')

    def test_map(self):
        #same as the last test
        app.get('/map')


    def test_new_user(self):
        self.app.test_client().get('/addUser')
        self.assert_template_used('addUser.html')

    def test_logout_template(self):
        self.app.test_client().get('/logout')
        self.assert_template_used('logout.html')
    
    #def test_login(self):
        

    def test_logout_login(self):
        with self.app.test_client().session_transaction() as session:
            self.app.test_client().get('/logout')
            self.assertFalse(session['logged_in'])'''

if __name__=='__main__':
        unittest.main()
