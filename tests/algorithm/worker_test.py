import pytest
import sure

from . import OttomenAlgorithmTestCase
from ottomen.algorithm.experiment import *
from ottomen.algorithm import globals
from ottomen.algorithm.worker import *
import random
import copy
from uuid import uuid1


class WorkerTestCase(OttomenAlgorithmTestCase):

    @classmethod
    def setUpClass(cls):
        super(WorkerTestCase, cls).setUpClass()
        cls.set_sizes = 500
        cls.set_limit = 200
        cls.worker_id = 'turkleton'
        cls.exp = new_experiment(1337, 0.98, set_limit=cls.set_limit, set_sizes=cls.set_sizes)
        db_worker = workers.save(Worker(id=cls.worker_id))
        cls.db_worker = db_worker
        cls.task = new_task('1337',     1337)
        cls.worker = workers.new_mem(1337, db_worker)
        cls.validated_qs_batch = 25
        cls.session_id = 'gaysession'
        cls.q_labels = {}

    def test_update_worker_tw_pos_correct(self):
        db_worker = workers.get(self.worker_id)
        prev_class_pos = db_worker.class_pos
        prev_class_neg = db_worker.class_neg
        random_q_ids = random.sample(self.exp.question_ids().members(), 15)
        qs = [self.exp.get_question(q_id) for q_id in random_q_ids]

        turk_answers = []
        for q in qs:
            r = random.randint(0, 3)
            if q['id'] not in self.q_labels:
                q_labels = []
                for i in range(0, r):
                    q_labels.append(str(uuid1()))
                q.validate({'label': len(q_labels) > 0, 'labels': q_labels})
                self.q_labels[q['id']] = q_labels
            else:
                q_labels = self.q_labels[q['id']]
            turk_answers.append({'question_id': q.question_id, 'labels': q_labels})

        self.worker.add_answers(self.session_id, *copy.deepcopy(turk_answers))
        answer_dict = {x['question_id']: x for x in turk_answers}
        update_worker_tw(self.exp.exp_id, self.db_worker, self.exp.get_questions(random_q_ids), answer_dict)
        db_worker = workers.get(self.worker_id)
        db_worker.tw_pos.should.equal(1.0, epsilon=0.000005)
        db_worker.tw_neg.should.equal(1.0, epsilon=0.000005)
        db_worker.class_pos.should.equal(min(globals.TW_SET_SIZE,
                                             prev_class_pos + sum(q.validation()['label'] for q in qs)))
        db_worker.class_neg.should.equal(min(globals.TW_SET_SIZE,
                                             prev_class_neg + sum(not q.validation()['label'] for q in qs)))

    def test_update_worker_tw_pos_correct_multiple_times(self):
        for i in range(0,10):
            self.test_update_worker_tw_pos_correct()

    def test_update_worker_tw_no_answers(self):
        w_id = 'mustafa'
        db_worker = workers.save(Worker(id=w_id))
        workers.new_mem(1337, db_worker)
        random_q_ids = random.sample(self.exp.question_ids().members(), 15)
        qs = [self.exp.get_question(q_id) for q_id in random_q_ids]

        turk_answers = []
        for q in qs:
            r = random.randint(0, 3)
            if q['id'] not in self.q_labels:
                q_labels = []
                for i in range(0, r):
                    q_labels.append(str(uuid1()))
                q.validate({'label': len(q_labels) > 0, 'labels': q_labels})
                self.q_labels[q['id']] = q_labels
            turk_answers.append({'question_id': q.question_id, 'labels': []})

        self.worker.add_answers(self.session_id, *copy.deepcopy(turk_answers))
        answer_dict = {x['question_id']: x for x in turk_answers}
        update_worker_tw(self.exp.exp_id, db_worker, self.exp.get_questions(random_q_ids), answer_dict)
        db_worker = workers.get(w_id)
        db_worker.tw_pos.shouldnt.equal(1.0, epsilon=0.000005)
        db_worker.tw_neg.should.equal(1.0, epsilon=0.000005)
        db_worker.banned.should.equal(True)

    def test_update_worker_tw_wrong_answers(self):
        w_id = 'mustafi'
        db_worker = workers.save(Worker(id=w_id))
        workers.new_mem(1337, db_worker)
        random_q_ids = random.sample(self.exp.question_ids().members(), 15)
        qs = [self.exp.get_question(q_id) for q_id in random_q_ids]

        turk_answers = []
        for q in qs:
            r = random.randint(0, 3)
            if q['id'] not in self.q_labels:
                q_labels = []
                for i in range(0, r):
                    q_labels.append(str(uuid1()))
                q.validate({'label': len(q_labels) > 0, 'labels': q_labels})
                self.q_labels[q['id']] = q_labels
            turk_answers.append({'question_id': q.question_id, 'labels': [str(uuid1())]})

        self.worker.add_answers(self.session_id, *copy.deepcopy(turk_answers))
        answer_dict = {x['question_id']: x for x in turk_answers}
        update_worker_tw(self.exp.exp_id, db_worker, self.exp.get_questions(random_q_ids), answer_dict)
        db_worker = workers.get(w_id)
        db_worker.tw_pos.shouldnt.equal(1.0, epsilon=0.000005)
        db_worker.tw_neg.shouldnt.equal(1.0, epsilon=0.000005)
        db_worker.banned.should.equal(True)


