# -*- coding: utf-8 -*-
from flask_sqlalchemy import Model
from sqlalchemy import orm
from sqlalchemy.orm.exc import UnmappedClassError
from flask_sqlalchemy import SQLAlchemy


class DefaultManager(object):
    """sqlalchemy 自定义管理器"""
    def __init__(self, model, session, sa):
        self.model = model
        self.session = session

        self.sa = sa
        self.query = self.model.query

    def sess_commit_rollback(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def create(self, **kwargs):
        """创建对象"""
        session = self.session
        if 'id' in kwargs:
            obj = session.query(self.model).get(kwargs['id'])
            if obj:
                return obj
        obj = self.model(**kwargs)
        session.add(obj)
        self.sess_commit_rollback()
        return obj


class _ManagerProperty(object):
    """管理器的 描述符"""
    def __init__(self, sa):
        self.sa = sa

    def __get__(self, obj, type):
        try:
            mapper = orm.class_mapper(type)
            if mapper:
                assert issubclass(type.Manager, self.sa.Manager), \
                    '{}不满足自定义管理器必须是{}的子类'.format(type.Manager, self.sa.Manager)
                return type.Manager(type, session=self.sa.session, sa=self.sa)
        except UnmappedClassError:
            return None


class _SessionProperty(object):
    """session会话描述符号"""
    def __init__(self, sa):
        self.sa = sa
        self.session = sa.session

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError('实例对象上没有这个属性')
        return self.session


class BaseModel(Model):
    """orm模型基类"""
    # 管理器的默认类
    Manager = None

    objects = None

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}

    def save(self):
        """保存一个实例对象"""
        session = type(self).session
        session.add(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e



class DefineSQLAlchemy(SQLAlchemy):
    """自定义sqlalchemy"""
    def __init__(self, *args, **kwargs):
        self.Manager = DefaultManager
        if 'manager' in kwargs:
            self.Manager = kwargs.pop('manager')
        if 'model_class' in kwargs:
            assert issubclass(kwargs['model_class'], BaseModel), '如果你使用了ext_manager, 那么你自定义的model_class' \
                                                                 '必须是{}的实例'.format(BaseModel)
        else:
            kwargs['model_class'] = BaseModel
        super().__init__(*args, **kwargs)

    def make_declarative_base(self, model, metadata=None):
        """重写此方法构造管理器objects对象"""
        rv = super().make_declarative_base(model, metadata)
        rv.session = _SessionProperty(self)
        rv.Manager = self.Manager
        rv.objects = _ManagerProperty(self)
        return rv


def ext_manager(sa=SQLAlchemy):
    """
    扩展 sa， 增加 manager
    return SQLAlchemy
    """
    def __init__(self, *args, **kwargs):
        self.Manager = DefaultManager
        if 'manager' in kwargs:
            self.Manager = kwargs.pop('manager')
        if 'model_class' in kwargs:
            assert issubclass(kwargs['model_class'], BaseModel), '如果你使用了ext_manager, 那么你自定义的model_class' \
                                                                 '必须是{}的实例'.format(BaseModel)
        else:
            kwargs['model_class'] = BaseModel
        super(self.__class__, self).__init__(*args, **kwargs)

    def make_declarative_base(self, model, metadata=None):
        """重写此方法构造管理器objects对象"""
        # rv = super().make_declarative_base(model, metadata)
        rv = super(self.__class__, self).make_declarative_base(model, metadata)

        # 给模型增加session属性
        rv.session = _SessionProperty(self)

        rv.Manager = self.Manager
        rv.objects = _ManagerProperty(self)

        return rv

    name = 'SQLAlchemy'
    bases = (sa,)
    class_dict = {
        '__init__': __init__,
        'make_declarative_base': make_declarative_base
    }
    rv = type(name, bases, class_dict)
    # SQLAlchemy.__init__ = __init__
    # SQLAlchemy.make_declarative_base = make_declarative_base
    return DefineSQLAlchemy
    # return rv
