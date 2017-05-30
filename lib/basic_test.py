from google.appengine.ext import ndb
import pytest

from models import GceSupportTickets


def test_GceSupportTickets():
    d = GceSupportTickets(day='Monday')
    assert 'Monday' == d.day
