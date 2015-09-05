# from backend.postgres.models import *
# from backend.postgres.database import db_session
# from backend.memory.experiment import worker as worker_mem, Experiment as Experiment_mem, Question as Question_mem
# from backend.memory.task import Task as Task_mem
# from backend.worker import update_worker
# from backend.question import update_questions

from ..resources.services import answers, experiments, questions, tasks, workers
from ..resources.models import Experiment, Session, Question, Validation, Worker
from .worker import update_worker
from .question import update_questions

from psycopg2 import IntegrityError
import datetime


def start_session(worker_id, task_id=1000):
    if worker_id is None or str(worker_id) == '':
        return {"session": {'completed': 'True', 'banned': 'True'}}

    worker_id = str(worker_id)
    worker_query = workers.filter(Worker.id == worker_id)

    # return {'worker_id' : worker_id}
    # TODO: implement this properly

    # Update from database
    if worker_query.count() == 0:
        worker = Worker(id=worker_id, timestamp=datetime.datetime.now())
    else:
        worker = worker_query.first()

    # check if experiment is completed
    task = tasks[task_id]
    exp_id = task['experiment_id']

    if worker.banned:
        return {"session": {'completed': 'True', 'banned': 'True'}}

    if experiments[exp_id]['completed'] == 'True':
        return {"session": {'completed': 'True'}}

    # Create a new session in the database
    session = Session(timestamp=datetime.datetime.now())
    session.worker_id = worker_id
    session.task_id = task_id
    try:
        db_session.add(session)
        db_session.add(worker)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()
        return {"session": {'completed': 'True', 'banned': 'True'}}
    if exp_id is None:
        return None
    worker_mem = workers.new_mem(exp_id, worker.as_dict())
    enough_questions = assign_questions(worker_mem, task, session.id)
    if not enough_questions:
        return {"session": {'completed': 'False', 'no_questions': 'True'}}

    else:
        return new_batch(worker_id, [], task_id, session.id)


def assign_questions(worker, task, session_id):
    exp = experiments[task['experiment_id']]
    if worker['class_neg'] == '1' and worker['class_pos'] == '1':
        question_set = list(exp.get_control_questions(task['initial_consensus']))
    else:
        question_set = list(questions.get_unanswered_consensus(
            task['experiment_id'],
            worker['id'],
            task['returning_consensus'])
        )

    questions_left = int(task['size']) - len(question_set)
    pos_amount = int(questions_left / 2)
    exp_questions = list(exp.get_questions_worker(worker['id'], questions_left))
    question_set.extend(exp_questions)
    if len(questions) < 20:
        return False
    else:
        worker.ask(session_id, question_set)
        return True


def new_batch(worker_id, answers, task_id, session_id):
    task = tasks[task_id]
    exp_id = task['experiment_id']
    worker = workers.get_mem(exp_id, worker_id)
    exp = experiments[exp_id]
    for answer in answers:
        answer['worker_id'] = worker_id

    question_set = worker.new_batch(session_id, answers, task['batch_size'])
    question_ids = [question_set["id"] for question in question_set if 'id' in question]

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

    if len(questions) == 0:
        pg_worker = update_worker(exp_id, session_id, worker_id)
        if not pg_worker.banned:
            validated_questions = update_questions(exp_id, worker_id, session_id, float(exp['accuracy']))
            update_sets(exp_id, validated_questions)
            store_validated_questions(worker_id, exp_id, validated_questions)
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
    new_questions.extend(questions.get_negative(exp_id, val_pos))


    # set the new questions to be in progress
    for question in new_questions:
        question.in_progress = True
        db_session.add(question)
    db_session.commit()

    if len(new_questions) > 0:
        exp = experiments[exp_id]
        exp.add_questions([q.as_dict(exp_id) for q in new_questions])


def store_validated_questions(worker_id, exp_id, validated_questions):
    pg_questions = questions.filter(Question.id.in_([x['id'] for x in validated_questions])).all()
    pg_dic = {x.id: x for x in pg_questions}
    pg_worker = workers.filter(Worker.id == worker_id).first()

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
        if 'malwares' in question:
            try:
                mws = eval(question['malwares'])
                if isinstance(mws, list) and len(mws) > 0:
                    val.malwares = answers.save_or_get_outputs(mws)
                    val.malware = len(val.malwares) > 0
            except TypeError:
                val.malware = False

        db_session.add(val)

        for answer in question['answers']:
            pg_ans = Answer(timestamp=datetime.datetime.now())
            pg_ans.worker_id = pg_worker.id
            pg_ans.malwares = val.malwares
            pg_ans.question_id = pg_q.id
            db_session.add(pg_ans)

        questions.get_mem(exp_id, question['id']).delete()

    # Experiment is complete
    if len(exp_mem.question_ids()) == 0:
        exp = experiments.filter(Experiment.id == exp_id).first()
        exp_mem['completed'] = True
        exp.completed = True
        db_session.add(exp)

    db_session.commit()


# this method clears the answers of this session from Redis
def clear_session(exp_id, worker_id, session_id):
    workers.get_mem(exp_id, worker_id).end_session(session_id)