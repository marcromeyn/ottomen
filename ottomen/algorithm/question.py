from scipy.stats import binom
from ..resources.services import experiments, workers, questions


def update_questions(exp_id, worker_id, session_id, accuracy):
    worker = workers.get_mem(exp_id, worker_id)
    answers = worker.session_answers(session_id)
    exp = experiments.get_mem(exp_id)

    validated_questions = []
    for answer in answers:
        if not exp.get_question(answer['question_id']).validation():
            question = exp.get_question_json(answer['question_id'])
            if question:
                question = evaluate(question, accuracy, exp_id)
                if 'validation' in question:
                    validated_questions.append(question)

    return validated_questions


# this method evaluates a question
def evaluate(question, accuracy, exp_id):
    mem_question = questions.get_mem(exp_id, question['id'])
    error = 1 - accuracy
    answers = mem_question.answers()
    question['answers'] = answers

    if len(answers) < 3:
        question['validated'] = False
        return question

    answers_workers = [{'answer': answer, 'worker': workers.get_mem_json(exp_id, answer['worker_id'])} for answer in answers]
    labels_count = {}

    all_workers = [x['worker'] for x in answers_workers]
    all_workers = [x for x in all_workers if (not x['banned'] and x['class_pos'] != 1)]

    for at_tuple in answers_workers:
        labels = at_tuple['answer']['labels']

        for label in labels.members():
            if label not in labels_count:
                labels_count[label] = 1
            else:
                labels_count[label] += 1

    x = len(answers)
    p_pos_min = min([worker['tw_pos'] for worker in all_workers])
    p_neg_min = min([worker['tw_neg'] for worker in all_workers])

    labels_class = {}
    labels = []
    for label in labels_count:
        n = labels_count[label]
        pos_likeliness = binom.cdf(n, x, p_pos_min)

        # then calc for !malware
        neg_likeliness = binom.cdf(x - n, x, p_neg_min)

        # positive confirmation

        if pos_likeliness > error > neg_likeliness:
            labels_class[label] = 1
            labels.append(label)
        # negative confirmation
        elif pos_likeliness < error < neg_likeliness:
            labels_class[label] = 0
        else:
            labels_class[label] = -1

    # all workers say there is not a single instance of malware
    neg_validation = False
    if len(labels_count) == 0:
        pos_likeliness = binom.cdf(0, x, p_pos_min)
        neg_likeliness = binom.cdf(x, x, p_neg_min)

        if pos_likeliness < error < neg_likeliness:
            neg_validation = True

    # only true if 1 or more labels are evaluated, or there are no labels and there is negative validation
    if (all(labels_class[label] != -1 for label in labels_class) and (len(labels_class) > 0)) or neg_validation:
        question['validation'] = {
            'label': len(labels) > 0,
            'labels': labels
        }

    return question
