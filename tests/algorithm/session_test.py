import pytest
import sure

from . import OttomenAlgorithmTestCase
from ottomen.algorithm.experiment import *
from ottomen.algorithm.session import *

class ExperimentTestCase(OttomenAlgorithmTestCase):

    def test_start_session_bad_worker(self):
        with pytest.raises(ApplicationError):
            start_session([], 1000)
        with pytest.raises(ApplicationError):
            start_session(12, 1000)
        with pytest.raises(ApplicationError):
            start_session(None, 1000)

    def test_start_session_bad_task(self):
        with pytest.raises(ApplicationError):
            start_session("turkturk", None)
        with pytest.raises(ApplicationError):
            start_session("turkturk", "bla")
        with pytest.raises(ApplicationError):
            start_session("turkturk", 0.2)

    def test_start_session(self):
        response = start_session("gayturkturk", 1000)



    # def test_start_session(self):
    #     response = start_session("turkyturk", 1000)
    #
    #
    # def test_get_pos_question_set(self):
    #     set_size = 500
    #     control_q_ids = get_control_question_ids()
    #     pos_questions = get_pos_question_set(set_size, control_q_ids)
    #     (len(pos_questions)).should.equal(set_size)
    #     for q in pos_questions:
    #         control_q_ids.shouldnt.contain(q)
    #
    # def test_get_neg_question_set(self):
    #     set_size = 500
    #     control_q_ids = get_control_question_ids()
    #     pos_questions = get_neg_question_set(set_size, control_q_ids)
    #     (len(pos_questions)).should.equal(set_size)
    #     for q in pos_questions:
    #         control_q_ids.shouldnt.contain(q)

    #
    # def test_initialize_sets(self):
    #     pass
    #
    # def test_set_questions(self):
    #     pass

