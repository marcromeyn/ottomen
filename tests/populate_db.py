import datetime
import csv
import sys
import os

from ottomen.resources.models import Experiment, Question, Label, Validation


def populate_db(session):
    if not os.environ.get('TRAVIS') or not os.environ.get('LOCAL'):
        base = os.path.dirname(os.path.abspath(__file__))
        path = base + '/fixtures/'
    else:  # For Docker
        path = '/code/tests/fixtures/'

    print 'starting db populate....'
    # experiments
    with open(path + 'experiment.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            exp = Experiment(**row)
            exp.id = int(row['id'])
            exp.completed = row['completed'] == 't'
            exp.end_date = None
            session.add(exp)

    # questions
    with open(path + 'question.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            q = Question(**row)
            q.id = int(row['id'])
            q.in_progress = row['in_progress'] == 't'
            q.belief = row['belief'] == 't'
            session.add(q)

    malwares = {}
    # malware
    with open(path + 'label.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            mw = Label(**row)
            mw.id = int(row['id'])
            mw.timestamp = datetime.datetime.now()
            malwares[row['id']] = mw
            session.add(mw)

    validations = {}
    # validations
    with open(path + 'validation.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            val = Validation(**row)
            val.label = row['label'] == 't'
            val.timestamp = datetime.datetime.now()
            validations[row['id']] = val
            session.add(val)

    # validation_malwares
    with open(path + 'validation_label.csv', 'r+') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            validations[row['validation_id']].labels.append(malwares[row['label_id']])

    session.commit()
    print 'complete'