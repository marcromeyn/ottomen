from ottomen.resources.services import *
import uuid


def create_experiment():
    some_experiment = {
        'description': "A shitty description",
        'accuracy': .7
    }

    exp = experiments.create(**some_experiment)
    exp.shouldnt.be(())
    exp.id.shouldnt.be(None)
    experiments.find(description=some_experiment['description']).shouldnt.be(())

    return exp


def create_worker():
    some_worker = {
        'id': str(uuid.uuid4())
    }
    worker = workers.create(**some_worker)
    worker.shouldnt.be(())
    worker.id.should_not.be.different_of(some_worker['id'])

    created_worker = workers.get(worker.id)
    created_worker.tw_pos.should.be.equal(1.0)
    created_worker.tw_neg.should.be.equal(1.0)
    created_worker.class_pos.should.be.equal(1)
    created_worker.class_neg.should.be.equal(1)

    return worker


def create_task():
    exp = create_experiment()
    some_task = {
        'id': str(uuid.uuid4()),
        'experiment': exp,
        'title': 'Some Tile',
        'description': 'Some shitty description',
        'url': 'http://juan-the-front-end-guy.com'
    }

    task = tasks.create(**some_task)
    task.shouldnt.be(())
    task.id.shouldnt.be(None)

    # Check defaults
    created_task = tasks.get(task.id)
    created_task.batch_size.should.be.equal(10)
    created_task.nr_of_batches.should.be.equal(5)
    created_task.size.should.be.equal(50)
    created_task.initial_consensus.should.be.equal(30)
    created_task.returning_consensus.should.be.equal(10)
    created_task.minimum_mt_score.should.be.equal(.95)
    created_task.minimum_mt_submissions.should.be.equal(500)
    created_task.reward.should.be.equal(.5)

    return task


def create_session():
    task = create_task()
    worker = create_worker()

    some_session = {
        'task': task,
        'worker': worker
    }

    session = sessions.create(**some_session)
    session.id.shouldnt.be(None)
    session.task.should.be(task)
    session.worker.should.be(worker)

    return session


def create_question():
    some_question = {
        'text': 'Who is the worst programmer in history?'
    }

    question = questions.create(**some_question)
    question.id.shouldnt.be(None)

    # Check defaults
    question.belief.should.be(True)
    question.in_progress.should.be(False)

    return question


def create_label(name='Label'):
    some_label = {
        'name': name
    }

    label = labels.create(**some_label)
    label.id.shouldnt.be(None)

    return label


def create_answer():
    question = create_question()
    worker = create_worker()
    label = create_label()

    some_answer = {
        'question': question,
        'worker': worker,
        'labels': [label]
    }

    answer = answers.create(**some_answer)
    answer.id.shouldnt.be(None)
    answer.worker.should.be(worker)
    answer.labels[0].name.should.be.equal(label.name)

    return answer
