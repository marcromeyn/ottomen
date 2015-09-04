from ...core import Service
from .models import Experiment


class ExperimentService(Service):
    __model__ = Experiment