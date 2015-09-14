from sqlalchemy import and_, not_

from ...core import db, Service, ServiceWithMem
from .models import Validation, Question
from ..models import Answer, Experiment
from .memory import QuestionMem


class ValidationService(Service):
    __model__ = Validation


class QuestionService(ServiceWithMem):
    __model__ = Question

    def get_mem(self, exp_id, question_id):
        return QuestionMem(exp_id, question_id)

    def get_mem_obj(self, exp_id, question_id):
        return self.new(**QuestionMem(exp_id, question_id).get())

    def get_mem_json(self, exp_id, question_id):
        return QuestionMem(exp_id, question_id).get()

    def new_mem(self, exp_id, question):
        validation = None
        control = False
        if type(question) is dict:
            validation = question.pop('validation', None)
            control = question.pop('control', False)
            question = self.new(**question)
        self._isinstance(question)

        ques_mem = QuestionMem(exp_id, question.id)
        question = ques_mem.to_hash(question)
        question['validation'] = validation
        question['control'] = control
        ques_mem.new(question)

        return ques_mem

    def update_mem(self, exp_id, question):
        if type(question) is dict:
            question = self.new(**question)
        return self.new_mem(exp_id, question)

    def get_unanswered_consensus(self, exp_id, worker_id, amount):
        from ..services import answers, validations

        val_q_subquery = validations.query()\
            .filter(Validation.experiment_id == exp_id).subquery()
        questions = self.query() \
            .join(val_q_subquery, Question.validations) \
            .filter(
                db.not_(
                    Question.id.in_(answers.filter(Answer.worker_id == worker_id))
                )
            )\
            .limit(amount).all()

        return questions

    def get_positive(self, exp_id, amount):
        positive_set = self \
            .query().filter(and_(Question.experiments.any(Experiment.id == exp_id),
                         and_(Question.belief, not_(Question.in_progress)))) \
            .limit(amount).all()

        return positive_set

    def get_negative(self, exp_id, amount, exp=None):
        negative_set = self \
            .query().filter(and_(Question.experiments.any(Experiment.id == exp_id),
                                        and_(not_(Question.belief), not_(Question.in_progress)))) \
            .limit(amount).all()

        return negative_set

    def get_control(self, exp_id, amount):
        questions = self.get_control_negative(exp_id, amount) + self.get_control_positive(exp_id, amount)
        return questions

    def get_control_positive(self, exp_id, amount):
        from ..services import validations

        val_q_subquery = validations.query().\
            filter(and_(Validation.experiment_id == exp_id, Validation.label)). \
            subquery()
        questions = self.query().join(val_q_subquery, Question.validations) \
            .limit(amount).all()

        return questions

    def get_control_negative(self, exp_id, amount):
        from ..services import validations

        val_q_subquery = validations.\
            query().filter(and_(Validation.experiment_id == exp_id, not_(Validation.label))). \
            subquery()
        questions = self.query().join(val_q_subquery, Question.validations) \
            .limit(amount).all()

        return questions

    @staticmethod
    def get_json_with_validation_info(question, exp_id):
        json = question.to_json()
        validations = [x for x in question.validations if x.experiment_id == int(exp_id)]
        if len(validations) > 0:
            json['validation'] = {
                'labels': [label.name for label in validations[0].labels],
                'label': validations[0].label
            }
        return json

    @staticmethod
    def get_validation_info(question, exp_id):
        dict = {}
        validations = [x for x in question.validations if x.experiment_id == int(exp_id)]
        if len(validations) > 0:
            dict['labels'] = [label.name for label in validations[0].labels]
            dict['label'] = validations[0].label
        dict['validated'] = len(validations) > 0
        return dict


