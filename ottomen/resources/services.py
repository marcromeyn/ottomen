from .accounts import AccountsService
from .answer import AnswerService, OutputService
from .experiment import ExperimentService
from .question import QuestionService, ValidationService
from .worker import WorkerService

accounts = AccountsService()
answers = AnswerService()
outputs = OutputService()
experiments = ExperimentService()
questions = QuestionService()
validations = ValidationService()
workers = WorkerService()
