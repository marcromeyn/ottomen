from ...core import mem, MemoryBase


class TaskMem(MemoryBase):
    def __init__(self, task_id):
        self.task_id = task_id

    def get(self):
        return mem.Hash("task.%s" % self.task_id)

    @staticmethod
    def new(task):
        task = task.to_json()
        mem.set("task.%s.experiment_id" % task['id'], task['experiment_id'])
        mem.Hash("task.%s" % task['id']).update(task)

        return TaskMem(task['id'])

    def experiment(self):
        from ..experiment import ExperimentMem
        exp_id = mem.get("task.%s.experiment_id" % self.task_id)

        return ExperimentMem(exp_id)
