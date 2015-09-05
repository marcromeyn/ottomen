from sqlalchemy import not_, and_

from ..resources.models import Question, Experiment, Validation
from ..resources.services import questions, experiments, validations

base_experiment_id = 0


def new_experiment(id, accuracy, description='', end_date=None, set_limit=400, set_sizes=1000, question_ids=None):
    exp = Experiment(id=id, accuracy=accuracy, description=description, end_date=end_date)
    experiments.save(exp)
    exp_mem = experiments.new_mem(exp.to_json())
    set_questions(exp, set_sizes, question_ids)
    initialize_sets(exp_mem, set_limit)

    return exp_mem


def set_questions(exp, set_sizes, question_ids):
    if question_ids is None or len(question_ids) == 0:
        control_qs = validations.filter(Validation.experiment_id == base_experiment_id).all()

        # positive examples
        question_set = questions.filter(
            and_(
                Question.belief,
                and_(
                    not_(Question.in_progress),
                    not_(Question.id.in_(control_qs))
                )
            ))\
            .limit(set_sizes).all()

        # negative examples
        question_set.extend(questions.filter(
            and_(
                not_(Question.belief),
                and_(
                    not_(Question.in_progress),
                    not_(Question.id.in_(control_qs))
                )
            ))
            .limit(set_sizes).all())

    else:
        question_set = questions.filter(Question.id.in_(question_ids)).all()
    exp.questions.extend(question_set)
    experiments.save(exp)

    return exp


def initialize_sets(exp, set_limit):
    positive_set = [positive.as_dict(exp.id) for positive in questions.get_positive(exp.id, set_limit)]
    negative_set = [negative.as_dict(exp.id) for negative in questions.get_negative(exp.id, set_limit)]

    # get control set from base experiment id
    control_set = questions.get_control(base_experiment_id, set_limit)

    # Saving the sets to Redis
    exp = experiments[exp.id]
    exp.add_questions(positive_set)
    exp.add_questions(negative_set)
    if len(control_set) > 0:
        exp.add_control_questions(control_set)

    return positive_set, negative_set, control_set
