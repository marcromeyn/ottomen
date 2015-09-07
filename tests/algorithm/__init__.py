import json

from werkzeug.test import Headers, Client

from ottomen.web.api import create_app
from .. import OttomenAppTestCase, settings


class OttomenAlgorithmTestCase(OttomenAppTestCase):

    @classmethod
    def setUpClass(cls):
        super(OttomenAlgorithmTestCase, cls).setUpClass()
        cls._create_fixtures()

