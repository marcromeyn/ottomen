import pytest
import sure

from . import OttomenAlgorithmTestCase
from ..factories import AccountFactory
from ottomen.algorithm.experiment import *
from ottomen.resources import services


class ExperimentTestCase(OttomenAlgorithmTestCase):

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
            control_q_ids.shouldnt.contain(q)

    def test_get_neg_question_set(self):
        set_size = 500
        control_q_ids = get_control_question_ids()
        pos_questions = get_neg_question_set(set_size, control_q_ids)
        (len(pos_questions)).should.equal(set_size)
        for q in pos_questions:
            control_q_ids.shouldnt.contain(q)

    #
    # def test_initialize_sets(self):
    #     pass
    #
    # def test_set_questions(self):
    #     pass
