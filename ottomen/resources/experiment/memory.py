from ...core import mem, MemoryBase
import uuid
from ...helpers import TypedSet


class ExperimentMem(MemoryBase):
    def __init__(self, exp_id):
        self.exp_id = exp_id

    def get(self):
        return self.parse_hash(self._hash())

    def new(self, experiment):
        self._hash().update(self.to_hash(experiment))

    def get_question_json(self, question_id):
        if question_id not in self.question_ids() and \
                        question_id not in self.control_question_ids():
            raise KeyError

        return self.parse_hash(self._question_hash(question_id))

    def get_question(self, id):
        from ..services import questions
        return questions.get_mem(self.exp_id, id)

    def get_questions(self, ids):
        return [self.get_question_json(question_id) for question_id in ids]

    def get_control_questions(self, amount):
        ids = self.control_question_ids().random(amount)
        return [self.get_question_json(q_id) for q_id in ids]

    def get_questions_worker(self, worker_id, amount):
        from ..services import workers
        worker = workers.get_mem(self.exp_id, worker_id)
        past_questions = worker.past_question_ids()
        unique_id = uuid.uuid4()
        question_ids = self.question_ids().diffstore(unique_id, past_questions).random(amount)

        # clear temporary set in Redis
        mem.Set(unique_id).clear()
        return self.get_questions(question_ids)

    def add_question(self, question):
        from ..services import questions
        ques_mem = questions.new_mem(self.exp_id, question)
        if type(question) is dict and 'control' in question \
                and question['control']:
            self.control_question_ids().add(question.id)
        else:
            self.question_ids().add(question.id)

        return ques_mem

    def add_questions(self, question_list):
        for question in question_list:
            self.add_question(question)

    def question_ids(self):
        return TypedSet("experiment.%s.question_ids" % self.exp_id)

    def control_question_ids(self):
        return TypedSet("experiment.%s.control_question_ids" % self.exp_id)

    def workers_active_ids(self):
        return TypedSet("experiment.%s.active_workers" % self.exp_id)

    def workers_sorted_tw_pos(self):
        return mem.ZSet("experiment.%s.workers_sorted_tw_pos" % self.exp_id)

    def workers_sorted_tw_neg(self):
        return mem.ZSet("experiment.%s.workers_sorted_tw_neg" % self.exp_id)

    def is_completed(self):
        return len(self.question_ids()) == 0

    def delete(self):
        # TODO: delete questions + workers
        self.question_ids().clear()
        self.control_question_ids().clear()
        self.workers_active_ids().clear()
        self.workers_sorted_tw_pos().clear()
        self.workers_sorted_tw_neg().clear()
        self._hash().clear()

    def _hash(self):
        return mem.Hash("experiment.%s" % self.exp_id)

    def _question_hash(self, question_id):
        return mem.Hash("experiment.%s.question.%s" % (self.exp_id, question_id))
