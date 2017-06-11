# -*- coding: utf-8 -*-
"""

*******************

"""

from email.utils import getaddresses, parseaddr
import os
import json
import jinja2
import pytz
import webapp2
import logging

# Cloud Datastore NDB model imports
from models import EmailMessages


# AppEngine Imports
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import users
from google.appengine.ext import ndb

# initialize Jinja + Jinja Filters
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# JSON parse filter
JINJA_ENVIRONMENT.filters['tojson'] = json.dumps

def datefilter(value, format="%Y-%m-%d"):
    # timezone you want to convert to from UTC
    tz = pytz.timezone('US/Pacific')
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

# Date filter
JINJA_ENVIRONMENT.filters['datefilter'] = datefilter


# Basehandler class for inheritance
class _BaseHandler(webapp2.RequestHandler):
    """Insert class comment here."""

    def initialize(self, request, response):
        super(_BaseHandler, self).initialize(request, response)

        try:
            self.user = users.get_current_user()

        except:
            print 'get user failed'

        self.template_variables = {}


class NotFoundPageHandler(_BaseHandler):
    """Insert class comment here."""

    def get(self):
        self.error(404)

        person = self.user

        template = JINJA_ENVIRONMENT.get_template('404.template')
        self.response.out.write(template.render(self.template_variables,
                                                person=person))


class HomePage(_BaseHandler):
    """Insert class comment here."""

    def get(self):
        logging.info('HomePage class requested')
        self.template_variables = {}
        template = JINJA_ENVIRONMENT.get_template(
            'home.template')

        self.template_variables['item'] = [{'sender': item.sender,
                                            'to': item.to,
                                            'cc': item.cc,
                                            'subject': item.subject,
                                            'html_body': item.html_body,
                                            'plain_body': item.plain_body,
                                            'created': item.created,
                                            'created_date': item.created_date,
                                            'key': item.key.urlsafe()} for item in EmailMessages.query(ancestor=ndb.Key(EmailMessages, 'default')).fetch()]

        self.response.write(template.render(self.template_variables))


class TaskDelete(_BaseHandler):
    """Insert class comment here."""

    def post(self):
        logging.info('HomePage posted')
        parent_key = ndb.Key(urlsafe=self.request.get('key'))
        item = parent_key.get()
        item.key.delete()

        self.redirect('/')


class HandleEmail(InboundMailHandler):

    def post(self):
        # create email message and parse out fields
        message = mail.InboundEmailMessage(self.request.body)

        # list of emails: ['blah@example.com', ...]
        to = [addr[1] for addr in getaddresses([message.to])]
        cc = [addr[1] for addr in getaddresses([getattr(message, 'cc', '')])]

        sender = parseaddr(message.sender)[1]
        subject = getattr(message, 'subject', '')

        html_body = ''
        for _, body in message.bodies('text/html'):
            html_body = body.decode()

        plain_body = ''
        for _, plain in message.bodies('text/plain'):
            plain_body = plain.decode()

        # Attachements are a list of tuples: (filename, EncodedPayload)
        # EncodedPayloads are likely to be base64
        #
        # EncodedPayload:
        # https://cloud.google.com/appengine/docs/python/refdocs/google.appengine.api.mail#google.appengine.api.mail.EncodedPayload
        #
        attachments = []

        for attachment in getattr(message, 'attachments', []):
            encoding = attachment[1].encoding
            payload = attachment[1].payload

            if (not encoding or encoding.lower() != 'base64'):
                payload = attachment[1].decode().encode('base64')

            attachments.append({
                'filename': attachment[0],
                'payload': payload
            })

        # logging, remove what you find to be excessive
        logging.info('From <%s> to [<%s>]', sender,  '>, <'.join(to))
        logging.info('Subject: %s', subject)
        logging.info('Body: %s', plain_body)
        logging.info('Attachments: %s', [a['filename'] for a in attachments])

        payload = json.dumps({
            'sender': sender,
            'to': to,
            'cc': cc,
            'subject': subject,
            'html_body': html_body,
            'plain_body': plain_body
        })

        parent_key = ndb.Key(EmailMessages, 'default')
        item = EmailMessages(parent=parent_key)
        item.sender = str(sender)
        item.to = str(to)
        item.cc = str(cc)
        item.subject = subject
        item.html_body = html_body
        item.plain_body = plain_body

        try:
            item.put()
            logging.info('Datastore EmailMessages write successful')
        except:
            logging.warning('Datastore EmailMessages write FAILED!')
