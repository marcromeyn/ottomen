import json

from werkzeug.test import Headers, Client

from ottomen.web.api import create_app
from .. import OttomenAppTestCase, settings


class OttomenAlgorithmTestCase(OttomenAppTestCase):
    def setUpClass(self):
        super(OttomenAlgorithmTestCase, self).setUp()
        self._create_fixtures()

