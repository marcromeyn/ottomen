import json

from werkzeug.test import Headers, Client

from ottomen.web.api import create_app
from .. import OttomenAppTestCase, settings


class OttomenResourceTestCase(OttomenAppTestCase):
    def setUp(self):
        super(OttomenResourceTestCase, self).setUp()
        # self.token = self._login()

