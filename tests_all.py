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

your_machine = platform.system()

if your_machine == 'Linux':

    # Setup additional paths for importing modules specific to GAE
    sys.path.insert(
        0,
        '/usr/local/google/home/afeddersen/google-cloud-sdk/platform/google_appengine')
    sys.path.insert(
        0,
        '/usr/local/google/home/afeddersen/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
    sys.path.insert(0, '/usr/local/google/home/afeddersen/repos/convoy/lib')
    sys.path.insert(0, '/usr/local/lib/python2.7/dist-packages')
    sys.path.insert(0, '/usr/local/google/home/afeddersen/repos/convoy')

elif your_machine == 'Darwin':

    # Setup additional paths for importing modules specific to GAE
    sys.path.insert(
        0, '/Users/afeddersen/google-cloud-sdk/platform/google_appengine')
    sys.path.insert(
        0, '/Users/afeddersen/google-cloud-sdk/platform/google_appengine/lib/yaml/lib')
    sys.path.insert(0, '/Users/afeddersen/repos/convoy/lib')

else:
    print """This test is configured for the laptop and workstation of afeddersen@
             If you receive this message that means your system paths are not
             configured correctly."""

from google.appengine.ext import testbed
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import webapp as webapp2

from mock import patch

from apiclient.http import HttpMockSequence

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

    def testGceAdminSnippetCreatePageGet(self):
        request = webapp2.Request.blank('/admin_snippet_create')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testAdminPageGet(self):
        request = webapp2.Request.blank('/admin')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceArcusCherrypicksPageGet(self):
        request = webapp2.Request.blank('/gce_arcus_cherrypicks')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceArcusCodeHealthPageGet(self):
        request = webapp2.Request.blank('/gce_arcus_code_health')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceArcusEstimationPageGet(self):
        request = webapp2.Request.blank('/gce_arcus_estimation')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceArcusTestMetricsEMailPageGet(self):
        request = webapp2.Request.blank('/gce_arcus_test_metrics_email')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceArcusTestMetricsPageGet(self):
        request = webapp2.Request.blank('/gce_arcus_test_metrics')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceArcusBlockingBugsPageGet(self):
        request = webapp2.Request.blank('/gce_arcus_blocking_bugs')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGceLaunchTimelinePageGet(self):
        request = webapp2.Request.blank('/gce_launch_timeline')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGcePublicDocsPageGet(self):
        request = webapp2.Request.blank('/gce_public_docs')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testGcpFireHoseEmailPageGet(self):
        request = webapp2.Request.blank('/gcp_firehose')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)

    def testHomePageGet(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)


# Cloud Datastore NDB model imports
from models import Snippet
from models import GceArianeUpcoming
from models import GceArianePast
from models import GceSupportTickets
from models import HackerNewsGce
from models import HackerNewsEc2
from models import GcpBlog
from models import AwsBlog
from models import GceQualityPri
from models import GceQualityTickets
from models import GceQualityOpen
from models import GceBuildMetrics
from models import GceArcusTestMetricsDevFlaky
from models import GceArcusTestMetricsStagingFlaky
from models import GceDocMetrics
from models import GceApiMetricsTop
from models import GceApiMetricsTopErrors
from models import GceStackOverflowUnanswered
from models import GceArcusCodeMetricsSum
from models import GceArcusCodeMetricsToDo
from models import GceArcusCodeMetricsDead
from models import GceArcusCodeMetricsFile
from models import GceArcusCodeMetricsLine
from models import GceLaunchTimeline
from models import GcpLastFourteenLaunches
from models import GcpNextFourteenLaunches
from models import GcpIncidents
from models import GcpP0Bugs
from models import GcpBugsByComp
from models import GcpNextEvent
from models import GcpSupportP0Open
from models import GcpSupportP0LastFourteen
from models import GcpTopTenAreaSize
from models import GcpTopTenTeamSize
from models import GcpCountAll
from models import GcpCountICs
from models import GcpCountManagers
from models import GcpCountDirectors
from models import GcpCountVPs
from models import GcpYearHired
from models import GcpCommonHire
from models import GcpArianeApprovers
from models import GceArcusTeam
from models import GceArcusCherryPath
from models import GceArcusCherryRelease
from models import GceArcusCherrySubTeam
from models import GceArcusCherryDetails
from models import GceArcusCherryAverage
from models import GceArcusCherryBugs


class datastoreTestCase(BaseTestCase):

    def testGceArianeUpcomingPut(self):
        i = GceArianeUpcoming(launch_date='Monday',
                              name='launch',
                              ariane_link='link',
                              owners='owner')
        i.put()
        self.assertEquals(i.launch_date, 'Monday')
        self.assertEquals(i.name, 'launch')
        self.assertEquals(i.ariane_link, 'link')
        self.assertEquals(i.owners, 'owner')

    def testGceSupportTicketsPut(self):
        i = GceSupportTickets(day='Monday', case_count=10)
        i.put()
        self.assertEquals(i.day, 'Monday')
        self.assertEquals(i.case_count, 10)


if __name__ == '__main__':
    unittest.main(verbosity=2)
