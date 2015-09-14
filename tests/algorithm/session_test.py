import pytest
import sure

from . import OttomenAlgorithmTestCase
from ottomen.algorithm.experiment import *
from ottomen.algorithm.session import *
from ottomen.algorithm import globals
from ottomen.resources.services import validations
import random
from uuid import uuid1

class SessionTestCase(OttomenAlgorithmTestCase):

    @classmethod
    def setUpClass(cls):
        super(SessionTestCase, cls).setUpClass()
        cls.set_sizes = 500
        cls.set_limit = 200
        cls.worker_id = 'turkleton'
        cls.exp = new_experiment(1337, 0.98, set_limit=cls.set_limit, set_sizes=cls.set_sizes)
        db_worker = workers.save(Worker(id="gayturk", tw_pos=0.9, class_pos=30, class_neg=30))
        cls.task = new_task('1337',1337)
        cls.worker = workers.new_mem(1337, db_worker)
        cls.validated_qs_batch = 25

    def test_start_session_bad_worker(self):
        start_session.when.called_with([], '1000').should.throw(ApplicationError)
        start_session.when.called_with(12, '1000').should.throw(ApplicationError)
        start_session.when.called_with(None, '1000').should.throw(ApplicationError)

    def test_start_session_bad_task(self):
        start_session.when.called_with('turkturk', None).should.throw(ApplicationError)
        start_session.when.called_with('turkturk', 1).should.throw(ApplicationError)
        start_session.when.called_with('turkturk', 0.2).should.throw(ApplicationError)

    def test_start_session(self):
        response = start_session("gayturkturk", '1337')

        response.should.have.key("session")
        response["session"].should.have.key("id")
        response["session"].should.have.key("completed")
        response["session"]["completed"].should.be(False)
        response["session"].should.have.key("banned")
        response["session"]["banned"].should.be(False)
        response["session"].should.have.key("task_id")
        response["session"].should.have.key("worker_id")
        response["session"]["task_id"].should.equal('1337')
        response["session"]["worker_id"].should.equal('gayturkturk')

        len(response["questions"]).should.be(globals.TASK_BATCH_SIZE)
        len(response["session"]["question_ids"]).should.be(globals.TASK_BATCH_SIZE)

        for question in response["questions"]:
            question.should.have.key("id")
            question["id"].should.be.an(int)
            question["text"].should.be.a(str)
            question["text"].shouldnt.be.empty()

    def start_new_batch_once(self, turk_answers=None, start_new_session=True, response=None):
        if start_new_session:
            response = start_session(self.worker_id, self.task['id'])

        if not turk_answers:
            turk_answers = []
            # randomly give some answers
            for question in response['questions']:
                answer = {'question_id': question['id'], 'labels': []}
                r = random.randint(0, 3)

                for i in range(0, r):
                    answer['labels'].append(str(uuid1()))
                turk_answers.append(answer)

        nb_response = new_batch(self.worker_id, answers, self.task['id'], response['session']['id'])
        nb_response["session"]["id"].should.equal(response['session']['id'])
        return nb_response

    def test_start_new_batch_once(self):
        nb_response = self.start_new_batch_once()
        nb_response.should.contain.key("session")
        nb_response.should.contain.key("questions")
        len(nb_response["questions"]).should.equal(globals.TASK_BATCH_SIZE)
        nb_response["session"]["worker_id"].should.equal(self.worker_id)
        nb_response["session"]["task_id"].should.equal(self.task['id'])
        len(nb_response["session"]["questions"]).should.equal(globals.TASK_BATCH_SIZE)
        len(nb_response["session"]["completed"]).should.equal(False)
        len(nb_response["session"]["banned"]).should.equal(False)

    def test_update_sets(self):
        old_q_ids = self.exp.question_ids()
        random_q_ids = random.shuffle(self.exp.question_ids())[:self.validated_qs_batch]
        qs = self.exp.get_questions(random_q_ids)

        for q in qs:
            q['validated'] = True

        update_sets(self.exp['id'], qs)

        new_q_ids = self.exp.question_ids()
        new_q_ids.remove(old_q_ids)

        new_qs = questions.filter(Question.id.in_(new_q_ids))
        for q in new_qs:
            q.in_progress.should.equal(True)

        new_qs = self.exp.get_questions(new_q_ids)

        (sum(nq['belief'] for nq in new_qs)).should.equal(rq['belief'] for rq in random_q_ids)
        (sum(not nq['belief'] for nq in new_qs)).should.equal(not rq['belief'] for rq in random_q_ids)

    def test_store_validated_questions(self):
        old_q_ids = self.exp.question_ids()
        random_q_ids = random.shuffle(self.exp.question_ids())[:self.validated_qs_batch]
        validated_questions = self.exp.get_questions(random_q_ids)

        # should add some labels to that stuff
        for q in validated_questions:
            q['validated'] = True
            q['labels'] = []
            r = random.randint(0, 3)
            # give every validated q one answer with one label
            for i in range(0, r):
                q['labels'].append(str(uuid1()))
            q['answers'] = [{"worker_id": "gayturk", "labels": q['labels']}]

        store_validated_questions("gayturk", self.exp['id'], validated_questions)

        # the random_q_ids should be removed now
        new_q_ids = self.exp.question_ids()
        for id in random_q_ids:
            new_q_ids.shouldnt.contain(id)

        new_q_ids.remove(old_q_ids)

        # get the questions and check if they are validated correctly
        db_questions = questions.filter(Question.id.in_(random_q_ids))
        len(db_questions).should.equal(len(random_q_ids))
        for q in validated_questions:
            db_q = next(db_q for db_q in db_questions if db_q.id == q['id'])
            len(db_q.validations).should.be.greater_than(0)
            validation = next(val for val in q.validations if val.experiment_id == self.exp['id'])

            # check if validation correct
            validation.label.should.equal(len(q['labels']) > 0)
            len(validation.labels).should.equal(q['labels'])
            for label in q['labels']:
                db_label = next(lb for lb in validation.labels if lb.name == label)
                db_label.shouldnt.be(None)

        # now check the answers
        for q in validated_questions:
            turk_answer = answers.filter(db.and_(Answer.worker_id == "gayturk", Answer.question_id == q['id']))
            turk_answer.should.exist
            len(turk_answer.labels).should.equal(len(q['labels']))
            for label in turk_answer.labels:
                turk_label = next(lb for lb in turk_answer.labels if lb.name == label)
                turk_label.shouldnt.be(None)

    def test_store_validated_qs_until_finish(self):
        """
        This method rus store_validated_questions until all the questions are validated and the experiment is completed.
        """
        nr_of_iters = (self.set_sizes * 2) / self.validated_qs_batch
        for i in range(0, nr_of_iters):
            self.test_store_validated_questions()

        # should be finished and no more questions
        self.exp['completed'].should.equal(True)
        self.exp.question_ids().should.be.empty
        db_exp = experiments.get(self.exp['id'])
        db_exp.completed.should.equal()



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

