from types import NoneType
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from .settings import REDIS_CONFIGURATION
# from flask_jwt import JWT
# from flask.ext.bouncer import Bouncer

from walrus import *

#: Flask-SQLAlchemy extension instance
db = SQLAlchemy()

# Init Redis
mem = Database(**REDIS_CONFIGURATION)

#: Flask-Mail extension instance
mail = Mail()

# jwt = JWT()
#
# bouncer = Bouncer()


class ApplicationError(Exception):
    """Base application error class."""

    def __init__(self, msg):
        self.msg = msg


class ApplicationFormError(Exception):
    """Raise when an error processing a form occurs."""

    def __init__(self, errors=None):
        self.errors = errors


class Service(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        kwargs.pop('latitude', None)
        kwargs.pop('longitude', None)
        return kwargs

    def save(self, *args, **kwargs):
        """Commits the models to the database and returns the models

        :param *args: the models to save
        :param **kwargs: the settings (commit)
        """
        commit = kwargs.pop('commit', True)
        for model in args:
            self._isinstance(model)
            db.session.add(model)
        if commit:
            db.session.commit()

        return [arg for arg in args] if len(args) > 1 else args[0]

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.query.all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs)

    def filter(self, the_filter):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter(the_filter).all()

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        model = self.new(**kwargs)
        model.created_at = datetime.datetime.now()
        # self._isinstance(model)
        return self.save(model)

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        model.modified_at = datetime.datetime.utcnow()
        self.save(model)
        return model

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()

    def query(self):
        return self.__model__.query

    def query_columns(self, *columns):
        return self.__model__.query.with_entities(*columns)


class ServiceWithMem(Service):
    """
    A service that also contains
    """

    def __getitem__(self, id):
        return self.get_mem(id)

    def get_mem(self, id):
        raise NotImplemented

    def get_mem_obj(self, id):
        raise NotImplemented

    def new_mem(self, obj):
        raise NotImplemented

    def update_mem(self, obj):
        raise NotImplemented


class MemoryBase:
    """
    Base class for the abstraction on top of Redis
    """
    def __getitem__(self, key):
        return self.get()[key]

    def __setitem__(self, key, value):
        return self.get().update({key: value})

    def get(self):
        raise NotImplemented

    def new(self, model):
        raise NotImplemented

    def update(self, model):
        raise NotImplemented

    def _add_types(self, model):
        not_str = {key: value for key, value in model.iteritems() if type(value) is not str}
        for key, value in not_str.iteritems():
            val_type = type(value)
            if val_type is int:
                model['_type_' + key] = 'int'
            elif val_type is float:
                model['_type_' + key] = 'float'
            elif val_type is long:
                model['_type_' + key] = 'long'
            elif val_type is bool:
                model['_type_' + key] = 'bool'
            elif val_type is datetime:
                model['_type_' + key] = 'datetime'
            elif val_type is NoneType:
                model['_type_' + key] = 'NoneType'

        return model

    def _parse_types(self, model):
        types = {key: value for key, value in model.iteritems() if key.startswith('_type_')}
        for key, val_type in types.iteritems():
            tkey = key[6:]
            model.pop(key, None)
            if val_type == 'int':
                model[tkey] = int(model[tkey])
            elif val_type == 'float':
                model[tkey] = float(model[tkey])
            elif val_type == 'long':
                model[tkey] = long(model[tkey])
            elif val_type == 'bool':
                if model[tkey] == 'True':
                    model[tkey] = True
                elif model[tkey] == 'None':
                    model[tkey] = None
                else:
                    model[tkey] = False
            elif val_type == 'datetime':
                # TODO: Parse date from str
                if model[tkey] == 'None':
                    model[tkey] = None
                else:
                    model[tkey] = model[tkey]
            elif val_type == 'NoneType':
                model[tkey] = None

        return model
