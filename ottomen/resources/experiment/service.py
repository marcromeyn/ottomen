from ...core import ServiceWithMem
from .models import Experiment
from .memory import ExperimentMem


class ExperimentService(ServiceWithMem):
    __model__ = Experiment

    def get_mem(self, id):
        return ExperimentMem(id)

    def new_mem(self, experiment):
        return ExperimentMem.new(experiment)