import pytest

from . import OttomenApiTestCase
from ..factories import AccountFactory
from ottomen.resources import services


class SessionApiTestCase(OttomenApiTestCase):
    def test_test(self):
        r = self.send_get_request('/session/test')
        db_session = self.db_session()

        self.assertOkJson(r)