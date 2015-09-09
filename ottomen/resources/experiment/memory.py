from ...core import mem, MemoryBase
import uuid


class ExperimentMem(MemoryBase):
    def __init__(self, exp_id):
        self.exp_id = exp_id

    def get(self):
        exp = self.parse_hash(mem.Hash("experiment.%s" % self.exp_id))
        if not exp:
            raise KeyError

        return exp

    def new(self, experiment):
        experiment = self.to_hash(experiment)
        mem.Hash("experiment.%s" % experiment['id']).update(experiment)

    def _question_hash(self, question_id):
        return mem.Hash("experiment.%s.question.%s" % (self.exp_id, question_id))

    def _control_question_hash(self, question_id):
        return mem.Hash("experiment.%s.control_question.%s" % (self.exp_id, question_id))

    def get_question_json(self, question_id):
        return self.parse_hash(self._question_hash(question_id))

    def get_questions(self, ids):
        return [self.get_question_json(question_id) for question_id in ids]

    def get_control_question(self, question_id):
        return self.parse_hash(self._control_question_hash(question_id))

    def get_control_questions(self, amount):
        ids = self.control_question_ids().random(amount)
        return [self.get_control_question(q_id).as_dict() for q_id in ids]

    def get_questions_worker(self, worker_id, amount):
        from ..services import workers
        worker = workers.get_mem(self.exp_id, worker_id)
        past_questions = worker.past_question_ids()
        unique_id = uuid.uuid4()
        question_ids = self.question_ids().diffstore(unique_id, past_questions).random(amount)

        # clear temporary set in Redis
        mem.Set(unique_id).clear()
        return self.get_questions(question_ids)

    def add_question(self, question, control=False):
        from ..services import questions
        if type(question) is dict:
            question = questions.new(**question)
            questions._isinstance(question)
        if not control:
            self._question_hash(question.id).update(self.to_hash(question))
            self.question_ids().add(question.id)
        else:
            self._control_question_hash(question.id).update(self.to_hash(question))
            self.control_question_ids().add(question.id)


    def add_questions(self, question_list, control=False):
        for question in question_list:
            self.add_question(question, control)

    def question_ids(self):
        return mem.Set("experiment.%s.question_ids" % self.exp_id)

    def control_question_ids(self):
        return mem.Set("experiment.%s.control_question_ids" % self.exp_id)

    def workers_active_ids(self):
        return mem.Set("experiment.%s.active_workers" % self.exp_id)

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
        self.get().clear()
