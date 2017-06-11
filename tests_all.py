# -*- coding: utf-8 -*-

"""Consolidated unit & functional tests for Convoy application

Usage:

$ python -S tests_all.py

Disable the import of the module site and the site-dependent manipulations
of sys.path that it entails using '-S'

https://docs.python.org/2/using/cmdline.html

"""

# Import modules from default python system paths
import os
import platform
import sys
import unittest
import logging
import sys


# Setup additional paths for importing modules specific to GAE
sys.path.insert(
    0, '/Users/afeddersen/google-cloud-sdk/platform/google_appengine')
sys.path.insert(
    0, '/Users/afeddersen/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(0, '/Users/afeddersen/repos/convoy/lib')


from google.appengine.ext import testbed
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp as webapp2

import webtest
import jinja2
import main


TEST_ROOT = os.path.dirname(os.path.realpath(__file__))

# Setup logging configuration
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

# ^^^ Unified above this point ^^^
# --- Cut below this point ---

app = main.app


class BaseTestCase(unittest.TestCase):
    # [START setup]

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_user_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_datastore_v3_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    # [START login]
    def loginUser(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)
    # [END login]

    # [END setup]

    def tearDown(self):
        self.testbed.deactivate()


class LoginTestCase(BaseTestCase):

    # [START test]
    def testLogin(self):
        self.assertFalse(users.get_current_user())
        self.loginUser()
        self.assertEquals(users.get_current_user().email(), 'user@example.com')
        self.loginUser(is_admin=True)
        self.assertTrue(users.is_current_user_admin())
    # [END test]


class HandlerTestCase(BaseTestCase):

    def testNotFoundPageGet(self):
        request = webapp2.Request.blank('/404')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 404)

    def testHomePageGet(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)


# Cloud Datastore NDB model imports
from models import EmailMessages


class datastoreTestCase(BaseTestCase):

    def testEmailMessagesPut(self):
        i = EmailMessages(sender='sender@example.com',
                          to='recipient@example.com',
                          cc='copy@example.com',
                          subject='subject',
                          html_body='html_body',
                          plain_body='plain_body')

        i.put()
        self.assertEquals(i.sender, 'sender@example.com')
        self.assertEquals(i.to, 'recipient@example.com')
        self.assertEquals(i.cc, 'copy@example.com')
        self.assertEquals(i.subject, 'subject')
        self.assertEquals(i.html_body, 'html_body')
        self.assertEquals(i.plain_body, 'plain_body')


if __name__ == '__main__':
    unittest.main(verbosity=2)
