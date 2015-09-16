from ..resources.models import Worker
from ..resources.services import experiments, workers
from .globals import TW_SET_SIZE, MIN_TW_WORKER


def update_worker(experiment_id, session_id, worker_id):
    worker = workers.get(worker_id)
    worker_mem = workers.get_mem(experiment_id, worker_id)

    answer_list = worker_mem.session_answers(session_id)
    answer_dict = {x['question_id']: x for x in answer_list}
    control = worker_mem.control(session_id)

    update_worker_tw(worker_mem.exp_id, worker, control, answer_dict)

    # save worker to postgres and then to Redis
    workers.save(worker)
    worker_mem.update(worker)

    return worker


def update_worker_tw(exp_id, worker, questions, answer_dict):
    neg_class_correct = 0
    neg_qs = 0
    pos_class_correct = 0
    pos_qs = 0

    for question in questions:
        answer = answer_dict[question['id']]
        answer_labels = answer['labels']
        if answer_labels is None:
            answer_labels = []

        validation = experiments[exp_id].get_question(question['id']).validation()
        question_labels = validation['labels']

        if not validation['label']:
            neg_qs += 1

            if len(answer_labels) == 0:
                neg_class_correct += 1

        else:
            pos_qs += 1
            # iterate over all the answers and see which are classified correctly
            if answer_labels > 0:
                correct = sum(x in question_labels for x in answer_labels)

            pos_class_correct += (float(correct) / float(len(question_labels)))

    # calc weights for neg_class
    if neg_qs != 0:
        old_neg_weight = float(worker.class_neg) / (worker.class_neg + neg_qs)
        new_neg_weight = float(neg_qs) / (worker.class_neg + neg_qs)
        new_tw = float(neg_class_correct) / neg_qs
        if neg_qs + worker.class_neg > TW_SET_SIZE:
            old_neg_weight = max(0, float(TW_SET_SIZE - neg_qs) / TW_SET_SIZE)
            new_neg_weight = min(1, float(neg_qs) / TW_SET_SIZE)

        worker.tw_neg = old_neg_weight * worker.tw_neg + new_neg_weight * new_tw
        worker.class_neg = min(TW_SET_SIZE, neg_qs + worker.class_neg)

    # calc weights for pos_class
    if pos_qs != 0:
        old_pos_weight = float(worker.class_pos) / (worker.class_pos + pos_qs)
        new_pos_weight = float(pos_qs) / (worker.class_pos + pos_qs)
        new_tw = float(pos_class_correct) / pos_qs
        if pos_qs + worker.class_pos > TW_SET_SIZE:
            old_pos_weight = max(0, float(TW_SET_SIZE - pos_qs) / TW_SET_SIZE)
            new_pos_weight = min(1, float(pos_qs) / TW_SET_SIZE)
        worker.tw_pos = old_pos_weight * worker.tw_pos + new_pos_weight * new_tw
        worker.class_pos = min(TW_SET_SIZE, pos_qs + worker.class_pos)

    if worker.tw_pos < MIN_TW_WORKER or worker.tw_pos < MIN_TW_WORKER:
        worker.banned = True

