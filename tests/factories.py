from factory import Sequence, LazyAttribute
from factory.alchemy import SQLAlchemyModelFactory

from ottomen.helpers import encrypt_password
from ottomen.core import db
from ottomen.resources import models


class AccountFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Account
        sqlalchemy_session = db.session

    email = Sequence(lambda n: 'user{0}@project.com'.format(n))
    username = Sequence(lambda n: 'user{0}'.format(n))
    password = LazyAttribute(lambda a: encrypt_password('password'))
    is_admin = False
