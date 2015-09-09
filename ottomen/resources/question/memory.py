from ...core import mem, MemoryBase


class QuestionMem(MemoryBase):
    def __init__(self, exp_id, question_id):
        self.question_id = question_id
        self.exp_id = exp_id

    def get(self):
        return self._parse_types(mem.Hash("experiment.%s.question.%s" % (self.exp_id, self.question_id)).as_dict())

    def new(self, question):
        question = self._add_types(question.to_json(redis=True))
        mem.Hash("experiment.%s.question.%s" % (self.exp_id, question['id'])).update(question)

    def answer_ids(self):
        return mem.Set("experiment.%s.question.%s.answer_ids" % (self.exp_id, self.question_id))

    def add_answer(self, answer):
        self.answer_ids().add(answer['id'])

        return self.get_answer(answer['id']).update(answer)

    def get_answer(self, answer_id):
        return mem.Hash("experiment.%s.question.%s.answer.%s" % (self.exp_id, self.question_id, answer_id))

    def answers(self):
        return [self.get_answer(answer_id).as_dict() for answer_id in self.answer_ids().members()]

    def experiment(self):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id)

    def delete(self):
        to_del = [self.get_answer(answer_id).clear() for answer_id in self.answer_ids().members()]
        self.answer_ids().clear()
        self.get().clear()