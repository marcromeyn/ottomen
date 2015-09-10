from ...core import mem, MemoryBase
from ottomen.helpers import TypedSet


class QuestionMem(MemoryBase):
    def __init__(self, exp_id, question_id):
        self.question_id = question_id
        self.exp_id = exp_id

    def get(self):
        return self.parse_hash(self._hash())

    def new(self, question):
        self._hash().update(self.to_hash(question))

    def answer_ids(self):
        return TypedSet("experiment.%s.question.%s.answer_ids" % (self.exp_id, self.question_id))

    def add_answer(self, answer):
        from ..services import answers

        if type(answer) is not dict:
            raise NotImplemented
        labels = answer.pop('labels', [])
        answer = answers.new(**answer)
        answers._isinstance(answer)

        self.answer_ids().add(answer['id'])
        self.answer_label_set(answer['id']).add(*labels)

        return self._answer_hash(answer['id']).update(answer)

    def get_answer(self, answer_id):
        answer = self.parse_hash(self._answer_hash(answer_id))
        answer['labels'] = self.answer_label_set(answer_id)

        return answer

    def answers(self):
        return [self.get_answer(answer_id) for answer_id in self.answer_ids().members()]

    def is_validated(self):
        if not self._validation_hash():
            return False
        else:
            return True

    def validate(self, validation):
        from ..services import validations

        if type(validation) is not dict:
            raise NotImplemented

        labels = validation.pop('labels', [])
        validation_model = validations.new(**validation)
        validations._isinstance(validation_model)

        self._validation_labels().add(*labels)
        self._validation_hash().update(validation)

        return validation()

    def validation(self):
        to_return = self.parse_hash(self._validation_hash())
        to_return['labels'] = self._validation_labels().members()

        return to_return

    def experiment(self):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id)

    def delete(self):
        for answer_id in self.answer_ids().members():
            self.get_answer(answer_id).clear()
        self.answer_ids().clear()
        self.get().clear()

    def answer_label_set(self, answer_id):
        return mem.Set("experiment.%s.question.%s.answer.%s.labels" % (self.exp_id, self.question_id, answer_id))

    def _hash(self):
        return mem.Hash("experiment.%s.question.%s" % (self.exp_id, self.question_id))

    def _validation_hash(self):
        return mem.Hash("experiment.%s.question.%s.validation" % (self.exp_id, self.question_id))

    def _validation_labels(self):
        return mem.Set("experiment.%s.question.%s.validation_labels" % (self.exp_id, self.question_id))

    def _answer_hash(self, answer_id):
        return mem.Hash("experiment.%s.question.%s.answer.%s" % (self.exp_id, self.question_id, answer_id))