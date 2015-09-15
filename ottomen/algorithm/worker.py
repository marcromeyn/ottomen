from ..resources.models import Worker
from ..resources.services import experiments, workers
from .globals import TW_SET_SIZE, MIN_TW_WORKER


def update_worker(experiment_id, session_id, worker_id):
    worker = workers.get(worker_id)
    worker_mem = workers.get_mem(experiment_id, worker_id)

    control_question_ids = worker_mem.control_question_ids(session_id)
    control = worker_mem.control(session_id)

    update_worker_tw(worker, control)

    # save worker to postgres and then to Redis
    workers.save(worker)
    worker_mem.update(worker)

    return worker


def update_worker_tw(worker, questions):
    # keep track of the score of the worker, ban the worker if he scores < 33%
    # print 'tw_pos_start %s, tw_neg_start: %s, class_neg_start: %s, class_pos_start: %s' % (
    #     worker.tw_pos, worker.tw_neg, worker.class_neg, worker.class_pos
    # )
    neg_class_correct = 0
    neg_qs = 0
    pos_class_correct = 0
    pos_qs = 0
    for question in questions:
        answer = eval(question['answer'])
        answer_malwares = answer['malwares']
        if answer_malwares is None:
            answer_malwares = []

        question_malwares = []
        if 'malwares' in question:
            question_malwares = eval(question['malwares'])

        if question['malware'] == 'False':
            neg_qs += 1

            if len(answer_malwares) == 0:
                neg_class_correct += 1

        else:
            pos_qs += 1
            # iterate over all the answers and see which are classified correctly
            if answer_malwares > 0:
                correct = sum(x in question_malwares for x in answer_malwares)

            pos_class_correct += (float(correct) / float(len(question_malwares)))

    # calc weights for neg_class
    if neg_qs != 0:
        old_neg_weight = (worker.class_neg) / (worker.class_neg+ neg_qs)
        new_neg_weight = float(neg_qs) / (worker.class_neg + neg_qs)
        new_tw = float(neg_class_correct) / neg_qs
        if neg_qs + worker.class_neg > TW_SET_SIZE:
            old_neg_weight = max(0, float(TW_SET_SIZE - neg_qs) / TW_SET_SIZE)
            new_neg_weight = min(1, neg_qs / TW_SET_SIZE)
        worker.tw_neg = old_neg_weight * worker.tw_neg + new_neg_weight * new_tw
        worker.class_neg = min(TW_SET_SIZE, neg_qs + worker.class_neg)

    # calc weights for pos_class
    if pos_qs != 0:
        old_pos_weight = (worker.class_pos) / (worker.class_pos + pos_qs)
        new_pos_weight = float(pos_qs) / (worker.class_pos + pos_qs)
        new_tw = float(pos_class_correct) / pos_qs
        if pos_qs + worker.class_pos > TW_SET_SIZE:
            old_pos_weight = max(0, float(TW_SET_SIZE - pos_qs) / TW_SET_SIZE)
            new_pos_weight = min(1, pos_qs / TW_SET_SIZE)
        worker.tw_pos = old_pos_weight * worker.tw_pos + new_pos_weight * new_tw
        worker.class_pos = min(TW_SET_SIZE, pos_qs + worker.class_pos)
    worker.tw_pos = min(1, worker.tw_pos)
    worker.tw_neg = min(1, worker.tw_neg)
    if worker.tw_pos < MIN_TW_WORKER or worker.tw_pos < MIN_TW_WORKER:
        worker.banned = True

