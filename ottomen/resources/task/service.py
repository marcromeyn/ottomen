from ...core import ServiceWithMem
from .models import Task
from .memory import TaskMem


class TaskService(ServiceWithMem):
    __model__ = Task

    def get_mem(self, id):
        return TaskMem(id)

    def new_mem(self, experiment):
        return TaskMem.new(experiment)