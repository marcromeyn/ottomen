from ...core import ServiceWithMem
from .models import Task
from .memory import TaskMem


class TaskService(ServiceWithMem):
    __model__ = Task

    def get_mem(self, id):
        return TaskMem(id)

    def new_mem(self, task):
        self._isinstance(task)
        task_mem = TaskMem(task.id)
        task_mem.new(task)

        return task_mem

    def update_mem(self, task):
        new_task = self.new(**task)
        return self.new_mem(new_task)