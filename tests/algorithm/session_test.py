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
        cls.set_sizes = 200
        cls.set_limit = 100
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
        len(response["session"]["questions"]).should.be(globals.TASK_BATCH_SIZE)

        for question in response["questions"]:
            question.should.have.key("id")
            question["id"].should.be.an(int)
            question["text"].should.be.a(str)
            question["text"].shouldnt.be.empty

    def start_new_batch_once(self, task=None, worker_id=None, turk_answers=None, start_new_session=True, response=None):
        if not worker_id:
            worker_id = self.worker_id

        if not task:
            task = self.task

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

        nb_response = new_batch(worker_id, turk_answers, task['id'], response['session']['id'])
        nb_response["session"]["id"].should.equal(response['session']['id'])
        return nb_response

    def test_new_batch_once(self, task=None, worker_id=None, start_new_session=True, turk_answers=None, response=None):
        if not worker_id:
            worker_id = self.worker_id
        if task is None:
            task = self.task
        nb_response = self.start_new_batch_once(task=task, worker_id=worker_id, start_new_session=start_new_session,
                                                turk_answers=turk_answers, response=response)
        nb_response.should.have.key("session")
        nb_response.should.have.key("questions")
        if start_new_session or len(nb_response['questions']) > 0:
            len(nb_response["questions"]).should.equal(globals.TASK_BATCH_SIZE)
            nb_response["session"]["worker_id"].should.equal(worker_id)
            nb_response["session"]["task_id"].should.equal(task['id'])
            len(nb_response["session"]["questions"]).should.equal(globals.TASK_BATCH_SIZE)
            nb_response["session"]["completed"].should.equal(False)
            nb_response["session"]["banned"].should.equal(False)
        return nb_response

    def test_new_batch_until_no_more_questions(self, task=None, worker_id=None, answer=None):
        previous_question_ids = []
        if worker_id is None:
            worker_id = self.worker_id

        if not task:
            task = self.task

        # run it till the end
        nr_of_sessions = 0

        while nr_of_sessions < 100:
            response = start_session(worker_id, task['id'])
            if 'no_questions' in response['session'] and response['session']['no_questions']:
                nr_of_sessions.should.be.greater_than(0)
                break
            batches = 0
            # we did start session and want to test the final one differently
            while not response['session']['completed'] and batches < 10:
                qs = response["questions"]
                for q in qs:
                    previous_question_ids.append(q['id'])
                answer_list = self.get_answer_list(qs, answer=answer)
                response = self.test_new_batch_once(task=task, worker_id=worker_id, start_new_session=False,
                                                    turk_answers=answer_list, response=response)
                # if not all(q['id'] not in previous_question_ids for q in response['questions']):
                #     bla = 'bla'
                # else:
                all(q['id'] not in previous_question_ids for q in response['questions']).should.equal(True)
                batches += 1

            # session ended
            batches.shouldnt.equal(0)
            batches.shouldnt.equal(10)
            response['session']['completed'].should.equal(True)
            response['session']['banned'].should.equal(False)
            response['questions'].should.be.empty
            nr_of_sessions += 1
        nr_of_sessions.shouldnt.equal(100)

    def test_new_batch_until_all_questions_validated(self):
        exp = new_experiment(2000, 0.98, set_limit=self.set_limit, set_sizes=self.set_sizes)
        task = new_task('2000', 2000)

        # 2 * sets * amount of qs required for validation / task size
        increment_estimate = (self.set_sizes * 2 * 8) / globals.TASK_BATCH_SIZE
        increment = 0
        while len(experiments.get_mem(exp.exp_id).question_ids().members()) > 50 and increment < 2 * increment_estimate:
            increment += 1
            worker_id = 'turkiturk%d' % increment
            self.test_new_batch_until_no_more_questions(task=task, worker_id=worker_id, answer=["the_label"])

        increment.shouldnt.equal(2 * increment_estimate)
        vals = validations.filter(Validation.experiment_id == exp.exp_id)
        len(vals).should.be.greater_than_or_equal_to(self.set_sizes * 2 - 50)
        for val in vals:
            len(val.labels).should.equal(1)
            val.labels[0].name.should.equal("the_label")
        for q in experiments.get(exp.exp_id).questions:
            if len(q.validations) > 0: # might be some unvalidated questions
                len(q.answers).should.be.greater_than_or_equal_to(3)
            turks = []
            for answer in q.answers:
                len(answer.labels).should.equal(1)
                answer.labels[0].name.should.equal("the_label")
                turks.shouldnt.contain(answer.worker_id)
                turks.append(answer.worker_id)

    def run_new_batch_until_no_more_questions(self, worker_id=None, empty=False, incorrect=False):
        previous_question_ids = []
        if worker_id is None:
            if empty:
                worker_id = 'emptyturk'
            if incorrect:
                worker_id = 'incorrectturk'
            else:
                worker_id = 'incredibleturk'

        response = start_session(worker_id, self.task['id'])

        # we did start session and want to test the final one differently
        batches = 0
        while not response['session']['completed'] and batches < 10:
            qs = response["questions"]
            for q in qs:
                previous_question_ids.append(q['id'])

            answer_list = self.get_answer_list(qs, empty=empty, incorrect=incorrect)
            response = self.test_new_batch_once(worker_id=worker_id, start_new_session=False,
                                                turk_answers=answer_list, response=response)
            all(q['id'] not in previous_question_ids for q in response['questions']).should.equal(True)
            batches += 1
        # session ended
        batches.shouldnt.equal(10)
        response['session']['completed'].should.equal(True)
        response['session']['banned'].should.equal(True)
        response['questions'].should.be.empty

    def test_run_new_batch_until_no_more_questions_empty(self):
        self.run_new_batch_until_no_more_questions(empty=True)

    def test_run_new_batch_until_no_more_questions_incorrect(self):
        self.run_new_batch_until_no_more_questions(incorrect=True)

    def get_answer_list(self, qs, answer=[], empty=False, incorrect=False):
        answer_list = []

        # give the correct answer
        for q in qs:
            if empty:
                label_list = []
            elif incorrect:
                label_list = ['tralalalala']
            elif q['validation']:
                label_list = list(q['validation']['labels'])
            else:
                label_list = answer
            answer_list.append({
                    'question_id': q['id'],
                    'labels': label_list
                })
        return answer_list


    def test_update_sets(self):
        old_q_ids = self.exp.question_ids().members()
        random.shuffle(old_q_ids)
        random_q_ids = old_q_ids[:self.validated_qs_batch]
        qs = self.exp.get_questions(random_q_ids)

        for q in qs:
            q['validated'] = True

        update_sets(self.exp['id'], qs)

        new_q_ids = self.exp.question_ids().members()
        new_q_ids = [id for id in new_q_ids if id not in old_q_ids]

        len(new_q_ids).should.equal(len(random_q_ids))

        new_qs = questions.filter(Question.id.in_(new_q_ids))
        for q in new_qs:
            q.in_progress.should.equal(True)

        new_qs = self.exp.get_questions(new_q_ids)

        (sum(nq['belief'] for nq in new_qs)).should.equal(sum(rq['belief'] for rq in qs))
        (sum(not nq['belief'] for nq in new_qs)).should.equal(sum(not rq['belief'] for rq in qs))

    def test_store_validated_questions(self):
        old_q_ids = self.exp.question_ids().members()
        random.shuffle(old_q_ids)
        random_q_ids = old_q_ids[:self.validated_qs_batch]

        validated_questions = self.exp.get_questions(random_q_ids)

        # should add some labels to that stuff
        for q in validated_questions:
            label_list = []
            r = random.randint(0, 3)
            # give every validated q one answer with one label
            for i in range(0, r):
                label_list

            q['validation'] = {
                'label': len(label_list) > 0,
                'labels': label_list
            }
            q['answers'] = [{"worker_id": "gayturk", "labels": label_list}]

        store_validated_questions(self.exp['id'], "gayturk", validated_questions)

        # the random_q_ids should be removed now
        new_q_ids = self.exp.question_ids().members()
        for id in random_q_ids:
            new_q_ids.shouldnt.contain(id)

        # get the questions and check if they are validated correctly
        db_questions = questions.filter(Question.id.in_(random_q_ids))
        len(db_questions).should.equal(len(random_q_ids))
        for q in validated_questions:
            db_q = next(db_q for db_q in db_questions if db_q.id == q['id'])
            len(db_q.validations).should.be.greater_than(0)
            validation = next(val for val in db_q.validations if val.experiment_id == self.exp['id'])

            # check if validation correct
            validation.label.should.equal(len(label_list) > 0)
            len(validation.labels).should.equal(len(label_list))
            for label in label_list:
                db_label = next(lb for lb in validation.labels if lb.name == label)
                db_label.shouldnt.be(None)

        # now check the answers
        for q in validated_questions:
            turk_answer = answers.filter(db.and_(Answer.worker_id == "gayturk", Answer.question_id == q['id']))[0]
            turk_answer.shouldnt.be(None)
            len(turk_answer.labels).should.equal(len(label_list))
            for label in q['labels']:
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
        exp = experiments[self.exp['id']]
        exp['completed'].should.equal(True)
        exp.question_ids().should.be.empty
        db_exp = experiments.get(self.exp['id'])
        db_exp.completed.should.equal(True)



