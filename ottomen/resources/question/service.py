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

    def new_mem(self, exp_id, question):
        return QuestionMem.new(exp_id, question)

    def get_unanswered_consensus(self, exp_id, worker_id, amount):
        from ..services import answers, validations

        val_q_subquery = validations.filter(Validation.experiment_id == exp_id).subquery()
        questions = self.query() \
            .join(val_q_subquery, Question.validations) \
            .filter(
                db.not_(
                    Question.id.in_(answers.filter(Answer.worker_id == worker_id).all())
                )
            )\
            .limit(amount).all()

        return [q.as_dict(exp_id) for q in questions]

    def get_positive(self, exp_id, amount):
        positive_set = self \
            .filter(and_(Question.experiments.any(Experiment.id == exp_id),
                         and_(Question.belief, not_(Question.in_progress)))) \
            .limit(amount).all()

        return positive_set

    def get_negative(self, exp_id, amount, exp=None):
        negative_set = self.filter(and_(Question.experiments.any(Experiment.id == exp_id),
                                        and_(not_(Question.belief), not_(Question.in_progress)))) \
            .limit(amount).all()

        return negative_set

    def get_control(self, exp_id, amount):
        questions = self.get_control_negative(exp_id, amount) + self.get_control_positive(exp_id, amount)
        return questions

        val_q_subquery = db_session.query(Validation). \
            filter(Validation.experiment_id == exp_id). \
            subquery()

        questions = db_session.query(Question) \
            .join(val_q_subquery, Question.validations) \
            .limit(amount).all()

        return [q.as_dict(exp_id) for q in questions]

    def get_control_positive(self, exp_id, amount):
        from ..services import validations

        val_q_subquery = validations.filter(and_(Validation.experiment_id == exp_id, Validation.malware)). \
            subquery()
        questions = self.query().join(val_q_subquery, Question.validations) \
            .limit(amount).all()

        return [q.as_dict(exp_id) for q in questions]

    def get_control_negative(self, exp_id, amount):
        from ..services import validations

        val_q_subquery = validations.filter(and_(Validation.experiment_id == exp_id, not_(Validation.malware))). \
            subquery()
        questions = self.query().join(val_q_subquery, Question.validations) \
            .limit(amount).all()

        return [q.as_dict(exp_id) for q in questions]
