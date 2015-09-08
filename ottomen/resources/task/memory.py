from ...core import mem, MemoryBase


class TaskMem(MemoryBase):
    def __init__(self, task_id):
        self.task_id = task_id

    def new(self, task):
        task = self._add_types(task.to_json(redis=True))
        mem.set("task.%s.experiment_id" % task['id'], task['experiment_id'])
        mem.Hash("task.%s" % task['id']).update(task)

    def get(self):
        return self._parse_types(mem.Hash("task.%s" % self.task_id).as_dict())

    def experiment(self):
        from ..experiment import ExperimentMem
        exp_id = mem.get("task.%s.experiment_id" % self.task_id)

        return ExperimentMem(exp_id)
