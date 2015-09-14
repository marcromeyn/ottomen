from sqlalchemy import not_, and_

from ..resources.models import Question, Experiment, Validation, Task
from ..resources.services import questions, experiments, validations, tasks

base_experiment_id = 0


def new_experiment(id, accuracy, description='', end_date=None, set_limit=400, set_sizes=1000, question_ids=None):
    exp = Experiment(id=id, accuracy=accuracy, description=description, end_date=end_date)
    experiments.save(exp)
    exp_mem = experiments.new_mem(exp)
    set_questions(exp, set_sizes, question_ids)
    initialize_sets(exp_mem, set_limit)

    return exp_mem


def new_task(id, exp_id, **kwargs):
    task = Task(id=id, experiment_id=exp_id, **kwargs)
    tasks.save(task)
    task_mem = tasks.new_mem(task)
    return task_mem


def set_questions(exp, set_sizes, question_ids):
    if question_ids is None or len(question_ids) == 0:
        question_set = get_question_set(set_sizes)
    else:
        question_set = get_questions(question_ids)

    exp.questions.extend(question_set)
    experiments.save(exp)

    return exp


def get_question_set(set_sizes):
    control_q_ids = get_control_question_ids()

    # positive examples
    question_set = get_pos_question_set(set_sizes, control_q_ids)

    # negative examples
    question_set.extend(get_neg_question_set(set_sizes, control_q_ids))
    return question_set


def get_control_question_ids():
    return [val.id for val in validations.query_columns(Validation.id)
            .filter(Validation.experiment_id == base_experiment_id).all()]


def get_pos_question_set(set_size, control_qs):
    qs = questions.query().filter(
        and_(
            Question.belief,
            and_(
                not_(Question.in_progress),
                not_(Question.id.in_(control_qs))
            )
        ))\
        .limit(set_size).all()
    return qs


def get_neg_question_set(set_size, control_qs):
    qs = questions.query().filter(
        and_(
            not_(Question.belief),
            and_(
                not_(Question.in_progress),
                not_(Question.id.in_(control_qs))
            )
        )).limit(set_size).all()
    return qs


def get_questions(question_ids):
    return questions.filter(Question.id.in_(question_ids)).all()


def initialize_sets(exp, set_limit):
    question_set = questions.get_positive(exp['id'], set_limit)
    question_set.extend(questions.get_negative(exp['id'], set_limit))

    # get control set from base experiment id
    control_set = [questions.get_json_with_validation_info(q, exp['id'])
                   for q in questions.get_control(base_experiment_id, set_limit)]
    
    # Saving the sets to Redis
    exp.add_questions(question_set)
    if len(control_set) > 0:
        exp.add_questions(control_set, control=True)

