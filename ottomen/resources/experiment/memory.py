from ...core import mem, MemoryBase


class ExperimentMem(MemoryBase):
    def __init__(self, exp_id):
        self.exp_id = exp_id

    # def get_questions_worker(self, worker_id, amount):
    #     worker = worker(self.exp_id, worker_id)
    #     past_questions = worker.past_question_ids()
    #     unique_id = uuid.uuid4()
    #     question_ids = self.question_ids().diffstore(unique_id, past_questions).random(amount)
    #
    #     # clear temporary set in Redis
    #     mem.Set(unique_id).clear()
    #     return self.get_questions(question_ids)

    def get(self):
        return mem.Hash("experiment.%s" % self.exp_id)

    @staticmethod
    def new(experiment):
        mem.Hash("experiment.%s" % experiment['id']).update(experiment)

        return ExperimentMem(experiment['id'])

    def get_question(self, question_id):
        return mem.Hash("experiment.%s.question.%s" % (self.exp_id, question_id))

    def get_questions(self, ids):
        return [self.get_question(question_id).as_dict() for question_id in ids]

    def add_questions(self, questions):
        if not questions:
            return
        # add the question ids to the question_ids
        ids = map(lambda x: x['id'], questions)
        self.question_ids().add(*ids)
        # Add the questions to the experiment
        for question in questions:
            self.get_question(question['id']).update(question)

    def get_control_question(self, question_id):
        return mem.Hash("experiment.%s.control_question.%s" % (self.exp_id, question_id))

    def get_control_questions(self, amount):
        ids = self.control_question_ids().random(amount)
        return [self.get_control_question(q_id).as_dict() for q_id in ids]

    def add_control_questions(self, questions):
        if not questions:
            return
        # add the question ids to the question_ids
        ids = map(lambda x: x['id'], questions)
        self.control_question_ids().add(*ids)
        # Add the questions to the experiment
        for question in questions:
            self.get_control_question(question['id']).update(question)

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
