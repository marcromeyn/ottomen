from scipy.stats import binom
from ..resources.services import experiments, workers, questions


def update_questions(exp_id, worker_id, session_id, accuracy):
    worker = workers.get_mem(exp_id, worker_id)
    answers = worker.session_answers(session_id)
    exp = experiments.get_mem(exp_id)

    validated_questions = []
    for answer in answers:
        question = exp.get_question_json(answer['question_id'])
        if question:
            question = evaluate(question, accuracy, exp_id)
            if question['validated']:
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

    answers_workers = [{'answer': answer, 'worker': workers.get_mem(exp_id, answer['worker_id'])} for answer in answers]
    malwares_count = {}

    all_workers = list(map(lambda y: y['worker'], answers_workers))
    all_workers = [x for x in all_workers if (x['banned'] == 'False' and x['class_pos'] != '1')]

    for at_tuple in answers_workers:
        mws = eval(at_tuple['answer']['malwares'])
        if isinstance(mws, list):
            for mw in mws:
                if mw != '[' and mw != ']':
                    if mw not in malwares_count:
                        malwares_count[mw] = 1
                    else:
                        malwares_count[mw] += 1

    x = len(answers)
    p_pos_min = min([float(worker['tw_pos']) for worker in all_workers])
    p_neg_min = min([float(worker['tw_neg']) for worker in all_workers])

    malwares_class = {}
    malwares = []
    for mw in malwares_count:
        n = malwares_count[mw]
        pos_likeliness = binom.cdf(n, x, p_pos_min)
        # then calc for !malware
        neg_likeliness = binom.cdf(x - n, x, p_neg_min)
        # positive confirmation

        if pos_likeliness > error > neg_likeliness:
            malwares_class[mw] = 1
            malwares.append(mw)
        # negative confirmation
        elif pos_likeliness < error < neg_likeliness:
            malwares_class[mw] = 0
        else:
            malwares_class[mw] = -1

    # all workers say there is not a single instance of malware
    neg_validation = False
    if len(malwares_count) == 0:
        pos_likeliness = binom.cdf(0, x, p_pos_min)
        neg_likeliness = binom.cdf(x, x, p_neg_min)

        # print 'pos_likeliness : binom.cdf(%s,%s,%s) = %s' % (0, x, p_pos_min, pos_likeliness)
        # print 'neg_likeliness : binom.cdf(%s,%s,%s) = %s' % (x, x, p_neg_min, neg_likeliness)

        if pos_likeliness < error < neg_likeliness:
            neg_validation = True

    # only true if 1 or more malwares are evaluated, or there are no malwares and there is negative validation
    if all(malwares_class[mw] != -1 for mw in malwares_class) and (len(malwares_class) > 0 or neg_validation):
        question['validated'] = True
        question['malware'] = len(malwares) > 0
        if len(malwares) > 0:
            question['malwares'] = malwares
    else:
        question['validated'] = False

    return question
