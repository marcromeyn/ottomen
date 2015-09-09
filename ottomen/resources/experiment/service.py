from ...core import ServiceWithMem
from .models import Experiment
from .memory import ExperimentMem


class ExperimentService(ServiceWithMem):
    __model__ = Experiment

    def get_mem(self, id):
        return ExperimentMem(id)

    def get_mem_obj(self, id):
        return self.new(**ExperimentMem(id).get())

    def get_mem_json(self, id):
        return ExperimentMem(id).get()

    def new_mem(self, experiment):
        if type(experiment) is dict:
            experiment = self.new(**experiment)
        self._isinstance(experiment)
        exp_mem = ExperimentMem(experiment.id)
        exp_mem.new(experiment)

        return exp_mem

    def update_mem(self, experiment):
        if type(experiment) is dict:
            experiment = self.new(**experiment)
        return self.new_mem(experiment)