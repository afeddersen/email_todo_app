# -*- coding: utf-8 -*-
"""main.py routes requests to the correct handler.

A note on naming:
* Cron handlers should end with '_cron'
* Cron handlers should be nested under the page they belong to

Todo:
    * No TODOs at this time

"""

import webapp2

app = webapp2.WSGIApplication([
    ('/_ah/mail/.+', 'base_page.HandleEmail'),
    ('/', 'base_page.HomePage'),
    ('/task_delete', 'base_page.TaskDelete'),
    ('/404', 'base_page.NotFoundPageHandler'),
    ('/.*', 'base_page.NotFoundPageHandler'),
], debug=True)
