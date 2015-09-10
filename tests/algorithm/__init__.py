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
        cls.exp = new_experiment(1337, 0.98)
        worker = workers.save(Worker(id="gayturk", tw_pos=0.9, class_pos=30, class_neg=30))
        new_task('1337',1337)
        workers.new_mem(1337, worker)
        # create experiment and task in redis


