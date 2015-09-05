from .accounts import AccountsService
from .answer import AnswerService, LabelService
from .experiment import ExperimentService
from .question import QuestionService, ValidationService
from .session import SessionService
from .task import TaskService
from .worker import WorkerService

experiments = ExperimentService()
answers = AnswerService()
labels = LabelService()
questions = QuestionService()
accounts = AccountsService()
sessions = SessionService()
tasks = TaskService()
validations = ValidationService()
workers = WorkerService()
