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
        # create experiment and task in redis
        exp = experiments.get(1000)
        experiments.new_mem(exp.to_json())
        task = tasks.get('1000')
        tasks.new_mem(task)

