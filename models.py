# -*- coding: utf-8 -*-
"""File that describes Cloud Datastore NDB models.

"""
import datetime

from google.appengine.ext import ndb


class EmailMessages(ndb.Model):
    sender = ndb.StringProperty(indexed=True)
    to = ndb.StringProperty(indexed=True)
    cc = ndb.StringProperty(indexed=True)
    subject = ndb.StringProperty(indexed=True)
    html_body = ndb.TextProperty()
    plain_body = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    created_date = ndb.DateProperty(auto_now_add=True)
