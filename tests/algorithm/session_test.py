import pytest
import sure

from . import OttomenAlgorithmTestCase
from ottomen.algorithm.experiment import *
from ottomen.algorithm.session import *
from ottomen.algorithm import globals

class ExperimentTestCase(OttomenAlgorithmTestCase):

    def test_start_session_bad_worker(self):
        start_session.when.called_with([], '1000').should.throw(ApplicationError)
        start_session.when.called_with(12, '1000').should.throw(ApplicationError)
        start_session.when.called_with(None, '1000').should.throw(ApplicationError)
        #
        # with pytest.raises(ApplicationError):
        #     start_session([], '1000')
        # with pytest.raises(ApplicationError):
        #     start_session(12, '1000')
        # with pytest.raises(ApplicationError):
        #     start_session(None, '1000')

    def test_start_session_bad_task(self):
        start_session.when.called_with('turkturk', None).should.throw(ApplicationError)
        start_session.when.called_with('turkturk', 1).should.throw(ApplicationError)
        start_session.when.called_with('turkturk', 0.2).should.throw(ApplicationError)
        #
        # with pytest.raises(ApplicationError):
        #     start_session("turkturk", None)
        # with pytest.raises(ApplicationError):
        #     start_session("turkturk", 1)
        # with pytest.raises(ApplicationError):
        #     start_session("turkturk", 0.2)

    def test_start_session(self):
        response = start_session("gayturkturk", '1000')

        response.should.have.key("session")
        response["session"].should.have.key("id")
        response["session"].should.have.key("completed")
        response["session"]["completed"].should.be(False)
        response["session"].should.have.key("banned")
        response["session"]["banned"].should.be(False)
        response["session"].should.have.key("task_id")
        response["session"].should.have.key("worker_id")
        response["session"]["task_id"].should.equal('1000')
        response["session"]["worker_id"].should.equal('gayturkturk')

        len(response["questions"]).should.be(globals.TASK_BATCH_SIZE)
        len(response["session"]["question_ids"]).should.be(globals.TASK_BATCH_SIZE)

        for question in response["questions"]:
            question.should.have.key("id")
            question["id"].should.be.an(int)
            question["text"].should.be.a(str)
            question["text"].shouldnt.be.empty()


    # def test_update_

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

