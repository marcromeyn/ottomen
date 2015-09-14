import json

from werkzeug.test import Headers, Client

from ottomen.web.api import create_app
from ottomen.resources.services import *
from ottomen.resources.models import Worker
from ottomen.algorithm.experiment import new_task, new_experiment
from .. import OttomenAppTestCase, settings


class OttomenAlgorithmTestCase(OttomenAppTestCase):

    @classmethod
    def setUpClass(cls):
        super(OttomenAlgorithmTestCase, cls).setUpClass()
        cls._create_fixtures()

        # create experiment and task in redis


