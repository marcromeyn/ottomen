from .accounts import AccountsService
from .answer import AnswerService, OutputService
from .experiment import ExperimentService
from .question import QuestionService, ValidationService
from .session import SessionService
from .task import TaskService
from .worker import WorkerService

accounts = AccountsService()
answers = AnswerService()
outputs = OutputService()
experiments = ExperimentService()
questions = QuestionService()
sessions = SessionService()
tasks = TaskService()
validations = ValidationService()
workers = WorkerService()
