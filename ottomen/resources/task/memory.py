from ...core import mem, MemoryBase


class TaskMem(MemoryBase):
    def __init__(self, task_id):
        self.task_id = task_id

    def new(self, task):
        task = self.to_hash(task)
        mem.set("task.%s.experiment_id" % task['id'], task['experiment_id'])
        self._hash().update(task)

    def get(self):
        return self.parse_hash(self._hash())

    def experiment(self):
        from ..experiment import ExperimentMem
        exp_id = mem.get("task.%s.experiment_id" % self.task_id)

        return ExperimentMem(exp_id)

    def _hash(self):
        return mem.Hash("task.%s" % self.task_id)
