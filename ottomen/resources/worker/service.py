from ...core import ServiceWithMem
from .models import Worker
from .memory import WorkerMem


class WorkerService(ServiceWithMem):
    __model__ = Worker

    def get_mem(self, exp_id, id):
        return WorkerMem(exp_id, id)

    def new_mem(self, experiment_id, worker):
        return WorkerMem.new(experiment_id, worker)