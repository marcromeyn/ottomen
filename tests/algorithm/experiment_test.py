import pytest
import sure

from . import OttomenAlgorithmTestCase
from ..factories import AccountFactory
from ottomen.algorithm.experiment import *
from ottomen.resources import services


class ExperimentTestCase(OttomenAlgorithmTestCase):

    def test_new_experiment(self):
        exp = new_experiment(1001, .95, 'testing', None, 400, 1000, None)
        exp.get()["id"].should.equal(1001)
        question_ids = exp.question_ids()
        control_question_ids = exp.control_question_ids()
        len(question_ids).should.equal(800)
        len(control_question_ids).should.be.greater_than(0)

        for id in control_question_ids:
            question_ids.shouldnt.contain(id)
        for id in question_ids:
            control_question_ids.shouldnt.contain(id)

        (experiments.get(1001)).id.should.equal(1001)
        experiments[1001].get()["id"].should.equal(1001)

    def test_new_task(self):
        new_experiment(1002, .95, 'testing', None, 400, 1000, None)
        task = new_task('1001', 1002, batch_size=10)
        task.get()["id"].should.equal('1001')
        task.get()["experiment_id"].should.equal(1002)
        tasks['1001'].get()['id'].should.equal('1001')

    def test_get_control_questions(self):
        control_qs = get_control_question_ids()
        (len(control_qs)).should.be.greater_than(10)
        (control_qs[0]).should.be.an('int')

    def test_get_pos_question_set(self):
        set_size = 500
        control_q_ids = get_control_question_ids()
        pos_questions = get_pos_question_set(set_size, control_q_ids)
        (len(pos_questions)).should.equal(set_size)
        for q in pos_questions:
            control_q_ids.shouldnt.contain(q.id)

    def test_get_neg_question_set(self):
        set_size = 500
        control_q_ids = get_control_question_ids()
        pos_questions = get_neg_question_set(set_size, control_q_ids)
        (len(pos_questions)).should.equal(set_size)
        for q in pos_questions:
            control_q_ids.shouldnt.contain(q.id)

    #
    # def test_initialize_sets(self):
    #     pass
    #
    # def test_set_questions(self):
    #     pass
