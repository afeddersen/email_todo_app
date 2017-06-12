# Import modules from default python system paths
import os
import platform
import sys
import unittest
import logging
import sys

# Setup additional paths for importing modules specific to GAE
sys.path.insert(
    0, '/Users/anthonyfeddersen/google-cloud-sdk/platform/google_appengine')
sys.path.insert(
    0,
    '/Users/anthonyfeddersen/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
sys.path.insert(0, '/lib')

from google.appengine.ext import testbed
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp as webapp2

import jinja2
import main

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


class HandlerTestCase(BaseTestCase):

    def testNotFoundPageGet(self):
        request = webapp2.Request.blank('/404')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 404)

    def testHomePageGet(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
