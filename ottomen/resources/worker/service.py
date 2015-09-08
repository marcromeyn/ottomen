from ...core import ServiceWithMem
from .models import Worker
from .memory import WorkerMem


class WorkerService(ServiceWithMem):
    __model__ = Worker

    def get_mem(self, exp_id, id):
        return WorkerMem(exp_id, id)

    def new_mem(self, exp_id, worker):
        self._isinstance(worker)
        worker_mem = WorkerMem(exp_id, worker.id)
        worker_mem.new(worker)

        return worker_mem

    def update_mem(self, exp_id, worker):
        new_worker = self.new(**worker)

        return self.new_mem(exp_id, new_worker)