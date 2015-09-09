import json

from werkzeug.test import Headers, Client

from ottomen.web.api import create_app
from ottomen.resources.services import *
from .. import OttomenAppTestCase, settings


class OttomenAlgorithmTestCase(OttomenAppTestCase):

    @classmethod
    def setUpClass(cls):
        super(OttomenAlgorithmTestCase, cls).setUpClass()
        cls._create_fixtures()
        exp = experiments.get(1000)
        experiments.new_mem(exp)
        task = tasks.get('1000')
        tasks.new_mem(task)
        # create experiment and task in redis


