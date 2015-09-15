from random import shuffle

from ...core import mem, MemoryBase
from ...helpers import TypedSet


class WorkerMem(MemoryBase):
    def __init__(self, exp_id, worker_id):
        self.worker_id = worker_id
        self.exp_id = exp_id

    def get(self):
        return self.parse_hash(self._hash())

    def new(self, worker):
        from ..experiment import ExperimentMem
        worker = self.to_hash(worker)
        exp = ExperimentMem(self.exp_id)
        exp.workers_active_ids().add(worker['id'])
        exp.workers_sorted_tw_pos().add(worker['id'], worker['tw_pos'])
        exp.workers_sorted_tw_neg().add(worker['id'], worker['tw_neg'])
        self._hash().update(worker)

    def ask(self, session_id, *questions):
        if not questions:
            raise ValueError

        from ..services import experiments
        for question in questions:
            ques_mem = experiments.get_mem(self.exp_id).add_question(question)
            question_id = ques_mem.get()['id']
            self.next_session_question_ids(session_id).add(question_id)
            if ques_mem.is_validated():
                self.control_question_ids(session_id).add(question_id)

    def new_batch(self, session_id, answers, number):
        for answer in answers:
            if not isinstance(answer, dict):
                raise TypeError

        from ..services import experiments
        if len(answers) > 0:
            self.add_answer(session_id, *answers)
            question_ids = [answer['question_id'] for answer in answers]
            self.next_session_question_ids(session_id).remove(*question_ids)
            self.past_question_ids().add(*question_ids)

        new_questions_ids = self.next_session_question_ids(session_id).random(number)
        batch = experiments.get_mem(self.exp_id).get_questions(new_questions_ids)
        shuffle(batch)

        return batch

    def add_answer(self, session_id, *answers):
        if not answers:
            raise ValueError

        from ..services import questions
        for answer in answers:
            answer['id'] = "%s_%s" % (session_id, answer['question_id'])
            answer['worker_id'] = self.worker_id
            questions.get_mem(self.exp_id, answer['question_id']).add_answer(answer)

            self.session_answer_ids(session_id).add(answer['id'])

    def get_answer(self, answer_id):
        from ..services import questions
        session_id, question_id = tuple(answer_id.split("_"))

        return questions.get_mem(self.exp_id, question_id).get_answer(answer_id)

        # questions.get_
        # return self.parse_hash(self._answer_hash(session_id, answer_id))

    def session_answers(self, session_id):
        return [self.get_answer(answer_id)
                for answer_id in self.session_answer_ids(session_id).members()]

    def delete_answer(self, answer_id):
        from ..services import questions
        session_id, question_id = tuple(answer_id.split("_"))
        questions.get_mem(self.exp_id, question_id).delete_answer(answer_id)

    def next_questions(self):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id).get_questions(self.next_question_ids().members())

    def past_questions(self):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id).get_questions(self.past_question_ids().members())

    def next_session_questions(self, session_id):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id).get_questions(self.next_session_question_ids(session_id))

    def control(self, session_id):
        from ..services import experiments
        return experiments.get_mem(self.exp_id).get_questions(self.control_question_ids(session_id).members())

    def end_session(self, session_id):
        from ..experiment import ExperimentMem
        exp = ExperimentMem(self.exp_id)
        exp.workers_active_ids().remove(self.worker_id)
        exp.workers_sorted_tw_pos().remove(self.worker_id)
        exp.workers_sorted_tw_neg().remove(self.worker_id)

        # check whether control questions have to deleted
        for question_id in self.control_question_ids(session_id).members():
            self.get_control_question(session_id, question_id).clear()
        self.control_question_ids(session_id).clear()

        # expire the past and next question sets
        exp_in_sec = 10000
        self.past_question_ids().expire(exp_in_sec)
        self.next_question_ids().expire(exp_in_sec)

    def ask_global(self, questions):
        return self.next_question_ids().add(*[question['id'] for question in questions])

    def session_answer_ids(self, session_id):
        return mem.Set("experiment.%s.worker.%s.%s.answers" % (self.exp_id, self.worker_id, session_id))

    def next_question_ids(self):
        return TypedSet("experiment.%s.worker.%s.next_question_ids" % (self.exp_id, self.worker_id))

    def past_question_ids(self):
        return TypedSet("experiment.%s.worker.%s.past_question_ids" % (self.exp_id, self.worker_id))

    def next_session_question_ids(self, session_id):
        return TypedSet("experiment.%s.worker.%s.%s.next_question_ids" % (self.exp_id, self.worker_id, session_id))

    def control_question_ids(self, session_id):
        return TypedSet("experiment.%s.worker.%s.%s.control_question_ids" %
                        (self.exp_id, self.worker_id, session_id))

    def delete(self):
        self.next_question_ids().clear()
        self.past_question_ids().clear()
        self.get().clear()

    def _hash(self):
        return mem.Hash("experiment.%s.worker.%s" % (self.exp_id, self.worker_id))
