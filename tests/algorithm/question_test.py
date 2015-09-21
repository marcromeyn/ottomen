import pytest
import sure

from . import OttomenAlgorithmTestCase
from ottomen.algorithm.experiment import *
from ottomen.algorithm import globals
from ottomen.algorithm.question import *
from ottomen.algorithm.worker import *
import numpy as np
import random
import copy
from uuid import uuid1


class QuestionTestCase(OttomenAlgorithmTestCase):

    @classmethod
    def setUpClass(cls):
        super(QuestionTestCase, cls).setUpClass()
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
        cls.nr_of_workers = 40
        cls.accuracy = 0.9
        cls.tw_pos = 0.9
        cls.tw_neg = 0.9
        cls.setUpWorkers()


    @classmethod
    def setUpWorkers(cls):
        for i in range(1, cls.nr_of_workers + 1):
            db_worker = workers.save(Worker(id=cls.worker_id + str(i), class_pos=20,
                                            class_neg=20, tw_pos=cls.tw_pos, tw_neg=cls.tw_neg))
            workers.new_mem(1337, db_worker)

    def test_evaluate_pos(self):
        validated = False
        for nr_of_labels in range(1,4):
            labels = []
            for j in range(0, nr_of_labels):
                labels.append('the_label%d' % j)
            for nr_of_answers in range(1, 10):
                answer_list = []
                question = self.exp.get_question_json(self.exp.question_ids()
                                                      .members()[nr_of_labels * 10 + nr_of_answers])

                for i in range(1, nr_of_answers + 1):
                    answer_list.append({
                        'id': 'answer' + str(i),
                        'question_id': question['id'],
                        'worker_id': self.worker_id + str(i),
                        'labels': copy.deepcopy(labels)
                    })

                for answer in answer_list:
                    self.exp.get_question(question['id']).add_answer(answer)

                for accuracy in np.arange(0.7, 1, 0.05):
                    if 'validation' in question:
                        question.pop('validation')
                    q_response = evaluate(question, accuracy, self.exp.exp_id)
                    n = x = len(answer_list)
                    pos_likeliness = binom.cdf(n, x, self.tw_pos)
                    neg_likeliness = binom.cdf(x - n, x, self.tw_neg)
                    if nr_of_answers < 3:
                        ('validation' in q_response).should.equal(False)
                    else:
                        ('validation' in q_response).should.equal(bool(pos_likeliness > 1 - accuracy > neg_likeliness))
                        if 'validation' in q_response:
                            q_response['validation']['label'].should.equal(len(labels) > 0)
                            len(q_response['validation']['labels']).should.equal(len(labels))
                            all(label in q_response['validation']['labels'] for label in labels).should.equal(True)

    def test_evaluate_neg(self):
        validated = False
        labels = []
        for nr_of_answers in range(1, 10):
            answer_list = []
            question = self.exp.get_question_json(self.exp.question_ids().members()[100 + nr_of_answers])

            for i in range(1, nr_of_answers + 1):
                answer_list.append({
                    'id': 'answer' + str(i),
                    'question_id': question['id'],
                    'worker_id': self.worker_id + str(i),
                    'labels': copy.deepcopy(labels)
                })

            for answer in answer_list:
                self.exp.get_question(question['id']).add_answer(answer)

            for accuracy in np.arange(0.7, 1, 0.05):
                if 'validation' in question:
                    question.pop('validation')
                q_response = evaluate(question, accuracy, self.exp.exp_id)
                x = len(answer_list)
                n = 0
                pos_likeliness = binom.cdf(n, x, self.tw_pos)
                neg_likeliness = binom.cdf(x - n, x, self.tw_neg)
                if nr_of_answers < 3:
                    ('validation' in q_response).should.equal(False)
                else:
                    ('validation' in q_response).should.equal(bool(pos_likeliness < 1 - accuracy < neg_likeliness))
                    if 'validation' in q_response:
                        q_response['validation']['label'].should.equal(len(labels) > 0)
                        len(q_response['validation']['labels']).should.equal(len(labels))






