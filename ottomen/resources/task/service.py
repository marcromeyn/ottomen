from ...core import ServiceWithMem
from .models import Task
from .memory import TaskMem


class TaskService(ServiceWithMem):
    __model__ = Task

    def get_mem(self, id):
        return TaskMem(id)

    def get_mem_obj(self, id):
        return self.new(**TaskMem(id).get())

    def get_mem_json(self, id):
        return TaskMem(id).get()

    def new_mem(self, task):
        if type(task) is dict:
            task = self.new(**task)
        self._isinstance(task)
        task_mem = TaskMem(task.id)
        task_mem.new(task)

        return task_mem

    def update_mem(self, task):
        if type(task) is dict:
            task = self.new(**task)
        return self.new_mem(task)