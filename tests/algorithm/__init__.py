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
        cls.set_sizes = 500
        cls.set_limit = 200
        cls.validated_qs_batch = 25
        cls.worker_id = 'turkleton'
        cls.exp = new_experiment(1337, 0.98, set_limit=cls.set_limit, set_sizes=cls.set_sizes)
        db_worker = workers.save(Worker(id="gayturk", tw_pos=0.9, class_pos=30, class_neg=30))
        cls.task = new_task('1337',1337)
        cls.worker = workers.new_mem(1337, db_worker)
        # create experiment and task in redis


