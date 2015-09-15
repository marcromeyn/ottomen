# from backend.postgres.models import *
# from backend.postgres.database import db_session
# from backend.memory.experiment import worker as worker_mem, Experiment as Experiment_mem, Question as Question_mem
# from backend.memory.task import Task as Task_mem
# from backend.worker import update_worker
# from backend.question import update_questions

from ..core import db
from ..resources.services import *
from ..resources.models import Answer, Experiment, Session, Question, Validation, Worker
from .worker import update_worker
from ..core import ApplicationError
from .question import update_questions
from ..settings import DEBUG

from psycopg2 import IntegrityError
import datetime


def start_session(worker_id, task_id=1000):
    if worker_id is None or not isinstance(worker_id, str):
        raise ApplicationError("Invalid worker_id")

    worker_res = workers.filter(Worker.id == worker_id)

    # Update from database
    if len(worker_res) == 0:
        worker = Worker(id=worker_id, timestamp=datetime.datetime.now())
    else:
        worker = worker_res[0]

    # check if experiment is completed
    task = tasks[task_id]
    if task_id is None or not isinstance(task_id, str) or task is None:
        raise ApplicationError("Invalid task_id")

    exp_id = task['experiment_id']

    if worker.banned:
        return {"session": {'banned': 'True'}}

    if experiments[exp_id]['completed'] == 'True':
        return {"session": {'experiment_completed': 'True'}}

    # Create a new session in the database
    session = Session(timestamp=datetime.datetime.now())
    session.worker_id = worker_id
    session.task_id = task_id
    sessions.save(session, commit=False)
    workers.save(worker, commit=False)
    db.session.commit()

    worker_mem = workers.new_mem(exp_id, worker)

    (enough_questions, question_set) = assign_questions(worker_mem, task, session.id)

    if not enough_questions:
        return {"session": {'completed': 'False', 'no_questions': 'True'}}
    else:
        return new_batch(worker_id, [], task_id, session.id)


def assign_questions(worker, task, session_id):
    exp = experiments[task['experiment_id']]

    # control questions
    if worker['class_neg'] == '1' and worker['class_pos'] == '1':
        question_set = list(exp.get_control_questions(task['initial_consensus']))
        for q in question_set:
            q['validation'] = exp.get_question(q['id']).validation()
    else:
        question_set = list(questions.get_unanswered_consensus(
            task['experiment_id'],
            worker['id'],
            task['returning_consensus'])
        )
        question_set = [questions.get_json_with_validation_info(q, exp['id']) for q in question_set]

    # not control questions
    questions_left = int(task['size']) - len(question_set)
    pos_amount = int(questions_left / 2)
    exp_questions = list(exp.get_questions_worker(worker['id'], questions_left))
    question_set.extend(exp_questions)
    if len(question_set) < 20:
        return False, question_set
    else:
        worker.ask(session_id, *question_set)
        return True, question_set


def new_batch(worker_id, answer_list, task_id, session_id):
    task = tasks[task_id]
    if task is None:
        return ApplicationError("Invalid task id")

    exp_id = task['experiment_id']
    exp = experiments[exp_id]

    worker = workers.get_mem(exp_id, worker_id)
    if worker is None:
        return ApplicationError("Invalid worker id")

    for answer in answer_list:
        answer['worker_id'] = worker_id

    question_set = worker.new_batch(session_id, answer_list, task['batch_size'])
    if DEBUG:
        for q in question_set:
            q['validation'] = exp.get_question(q['id']).validation()

    question_ids = [question["id"] for question in question_set]

    batch = {
        "session": {
            "id": session_id,
            "worker_id": worker_id,
            "task_id": task_id,
            "questions": question_ids,
            "completed": False,
            "banned": False
        },
        "questions": question_set,
    }

    if len(question_set) == 0:
        pg_worker = update_worker(exp_id, session_id, worker_id)
        if not pg_worker.banned:
            validated_questions = update_questions(exp_id, worker_id, session_id, float(exp['accuracy']))
            update_sets(exp_id, validated_questions)
            store_validated_questions(exp_id, validated_questions)
        else:
            batch["session"]['banned'] = True
        clear_session(exp_id, worker_id, session_id)
        batch["session"]['completed'] = True

    return batch


def update_sets(exp_id, validated_questions):
    # write all validated questions to Postgres and delete them from Redis
    val_pos = len([i for i in validated_questions if (i['validated'] and i['belief'])])
    val_neg = len(validated_questions) - val_pos

    new_questions = []
    new_questions.extend(questions.get_positive(exp_id, val_pos))
    new_questions.extend(questions.get_negative(exp_id, val_neg))


    questions.set_in_progress(new_questions)

    if len(new_questions) > 0:
        exp = experiments[exp_id]
        exp.add_questions(new_questions)


def store_validated_questions(worker_id, exp_id, validated_questions):
    pg_questions = questions.filter(Question.id.in_([x['id'] for x in validated_questions]))
    pg_dic = {x.id: x for x in pg_questions}
    pg_worker = workers.filter(Worker.id == worker_id)[0]

    exp_mem = experiments[exp_id]

    # remove the questions from the list of questions in the experiment
    if len(validated_questions) > 0:
        remove_ids = [str(q['id']) for q in validated_questions]
        exp_mem.question_ids().remove(*remove_ids)

    for question in validated_questions:
        pg_q = pg_dic[int(question['id'])]
        val = Validation()
        val.timestamp = datetime.datetime.now()
        val.question_id = pg_q.id
        val.experiment_id = exp_id
        val.labels = labels.save_or_get_labels(question['labels'])
        val.label = len(val.labels) > 0
        validations.save(val, commit=False)

        for answer in question['answers']:
            pg_ans = Answer(timestamp=datetime.datetime.now())
            pg_ans.worker_id = answer['worker_id']
            pg_ans.labels = labels.save_or_get_labels(answer['labels'])
            pg_ans.question_id = pg_q.id
            answers.save(pg_ans)

        questions.get_mem(exp_id, question['id']).delete()

    # Experiment is complete
    if len(exp_mem.question_ids()) == 0:
        exp = experiments.get(exp_id)
        exp.completed = True
        experiments.update_mem(exp)
        experiments.save(exp, commit=False)

    db.session.commit()


# this method clears the answers of this session from Redis
def clear_session(exp_id, worker_id, session_id):
    workers.get_mem(exp_id, worker_id).end_session(session_id)


