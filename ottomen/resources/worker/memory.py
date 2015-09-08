from random import shuffle

from ...core import mem, MemoryBase


class WorkerMem(MemoryBase):
    def __init__(self, exp_id, worker_id):
        self.worker_id = worker_id
        self.exp_id = exp_id

    def get(self):
        return self._parse_types(mem.Hash("experiment.%s.worker.%s" % (self.exp_id, self.worker_id)).as_dict())

    def new(self, worker):
        from ..experiment import ExperimentMem
        exp = ExperimentMem(self.exp_id)
        exp.workers_active_ids().add(worker['id'])
        exp.workers_sorted_tw_pos().add(worker['id'], worker['tw_pos'])
        exp.workers_sorted_tw_neg().add(worker['id'], worker['tw_neg'])
        mem.Hash("experiment.%s.worker.%s" % (self.exp_id, worker['id'])).update(worker)

    def session_answer_ids(self, session_id):
        return mem.Set("experiment.%s.worker.%s.%s.answers" % (self.exp_id, self.worker_id, session_id))

    def add_answer(self, session_id, answer):
        if not answer:
            return
        else:
            return self.get_answer(session_id, answer['id']).update(answer)

    def get_answer(self, session_id, answer_id):
        return mem.Hash("experiment.%s.worker.%s.%s.answer.%s" % (self.exp_id, self.worker_id, session_id, answer_id))

    def session_answers(self, session_id):
        return [self.get_answer(session_id, answer_id).as_dict()
                for answer_id in self.session_answer_ids(session_id).members()]

    def delete_answer(self, session_id, answer_id):
        return self.get_answer(session_id, answer_id).clear()

    def past_question_ids(self):
        return mem.Set("experiment.%s.worker.%s.past_question_ids" % (self.exp_id, self.worker_id))

    def past_questions(self):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id).get_questions(self.past_question_ids().members())

    def next_question_ids(self):
        return mem.Set("experiment.%s.worker.%s.next_question_ids" % (self.exp_id, self.worker_id))

    def next_questions(self):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id).get_questions(self.next_question_ids().members())

    def next_session_questions(self, session_id):
        from ..experiment import ExperimentMem
        return ExperimentMem(self.exp_id).get_questions(self.next_session_question_ids(session_id))

    def next_session_question_ids(self, session_id):
        return mem.Set("experiment.%s.worker.%s.%s.next_question_ids" % (self.exp_id, self.worker_id, session_id))

    def get_control_question(self, session_id, question_id):
        return mem.Hash("experiment.%s.worker.%s.%s.control_question.%s" %
                             (self.exp_id, self.worker_id, session_id, question_id))

    def control_question_ids(self, session_id):
        return mem.Set("experiment.%s.worker.%s.%s.control_question_ids" %
                            (self.exp_id, self.worker_id, session_id))

    def add_control_questions(self, session_id, questions):
        if not questions:
            return
        self.control_question_ids(session_id).add(*[question['id'] for question in questions])
        for question in questions:
           self.get_control_question(session_id, question['id']).update(question)

    def control(self, session_id):
        return [self.get_control_question(session_id, question_id).as_dict()
                for question_id in self.control_question_ids(session_id).members()]

    def end_session(self, session_id):
        from ..experiment import ExperimentMem
        exp = ExperimentMem(self.exp_id)
        exp.workers_active_ids().remove(self.worker_id)
        exp.workers_sorted_tw_pos().remove(self.worker_id)
        exp.workers_sorted_tw_neg().remove(self.worker_id)

        # delete session answers
        for answer_id in self.session_answer_ids(session_id).members():
            self.delete_answer(session_id, answer_id)

        # delete control questions
        for question_id in self.control_question_ids(session_id).members():
            self.get_control_question(session_id, question_id).clear()
        self.control_question_ids(session_id).clear()

        # expire the past and next question sets
        exp_in_sec = 10000
        self.past_question_ids().expire(exp_in_sec)
        self.next_question_ids().expire(exp_in_sec)

    # def update_answers(self, session_id, answers):
    #     if not answers:
    #         return
    #     for answer in answers:
    #         answer['id'] = str(session_id) + '_' + answer['question_id']
    #         if answer['question_id'] in self.control_question_ids(session_id).members():
    #             question_mem = self.get_control_question(session_id, answer['question_id'])
    #             question_mem.update({"answer": answer})
    #         else:
    #             question_mem = Question(self.exp_id, answer['question_id'])
    #             question_mem.add_answer(answer)
    #             self.add_answer(session_id, answer)
    #             self.session_answer_ids(session_id).add(answer['id'])

    def new_batch(self, session_id, answers, number):
        from ..experiment import ExperimentMem
        if len(answers) > 0:
            # self.update_answers(session_id, answers)
            question_ids = [answer['question_id'] for answer in answers]
            self.next_session_question_ids(session_id).remove(*question_ids)
            past_question_ids = [answer['question_id'] for answer in answers]
            self.past_question_ids().add(*past_question_ids)

        new_questions = self.next_session_question_ids(session_id).random(number)
        control_question_ids = self.control_question_ids(session_id).members()
        control_qs_ids_to_get = [x for x in new_questions if x in list(control_question_ids)]
        new_questions = [x for x in new_questions if x not in list(control_question_ids)]
        control_questions = [self.get_control_question(session_id, question).as_dict()
                             for question in control_qs_ids_to_get]
        others = ExperimentMem(self.exp_id).get_questions(new_questions)
        others.extend(control_questions)
        shuffle(others)
        return others

    def ask_global(self, questions):
        return self.next_question_ids().add(*[question['id'] for question in questions])

    def ask(self, session_id, questions):
        self.next_session_question_ids(session_id).add(*[question['id'] for question in questions])
        control = [question for question in questions if str(question['validated']) == "True"]
        self.add_control_questions(session_id, control)

    def delete(self):
        self.next_question_ids().clear()
        self.past_question_ids().clear()
        self.get().clear()
