## 说明	
> note:
最近项目上使用了falsk框架，发现 sqlalchemy 中的 Model中并没有像 django-orm中Model的管理器 objects， 但是我的Model中需要很多使用到当前Model的类方法， 比如基本的create 方法， 还有很多针对业务方面的方法，如果都放在 Model中显得模型类很乱，因此就想着能不能构造出一种django中的objects管理器，将这些方法放在管理器中。 但是新的问题出现了，就是管理器中需要用到当前的 Model， 如何将当前的Model传入管理器， 我们不可能针对每一个模型中都重新定义objects， 将当前Model传进去，这显然不是很优雅的解决方式，也不适合继承的方式。因此在查看了 django-orm的源码，发现了原来 django-orm采用的是元类编程，定义了一个 metaclass，动态的创建 Model，创建的过程中调用管理器中的方法，将当前 Model传进去了，因此objects中会有一个 model的属性。

## 元类编程简介(以下代码都是建立在python3中）
### 概念
- Python中所有的东西都是对象（如`str, int, dict, list, function, object, class`)
- Class()创建对象 instance， 那么Class类既然是对象，谁创建了类呢， 那就是type(元类)来创建类

```Python
class A(object):
    pass
a = A()

print(type('zc'), type([1,2]), type(a), type(A))
print('-'*50)
print(type(str), type(list), type(object), type(type))
```
> 输出：

    <class 'str'> <class 'list'> <class '__main__.A'> <class 'type'>
    --------------------------------------------------
    <class 'type'> <class 'type'> <class 'type'> <class 'type'>
    
- type有两个作用
	- `type('zc')`当传入一个参数的时候，是查看创建了参数对象的对象
	- `type(new_class_name, base_classes, new_class_attrs)`传入三个参数的时候，是动态的创建类
- 当在文件中通过 class 关键字的时候，默认是通过 type元类创建类
- 在 python3 中如果想通过元类type的子类， 包含type操作的函数作为元类来动态的创建类，可以如下：

```python3
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    """返回一个类对象，将属性都转为大写形式"""
    # 选择所有不以'__'开头的属性 列表(元祖)生成式
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    # 通过type来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)

class UpperMeta(type):
    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        # 通过type来做类对象的创建
        return type(future_class_name, future_class_parents, uppercase_attr)
# __metaclass__ = UpperMeta  # python2 中这会作用到这个模块中所有的类
class Foo(metaclass=upper_attr):
    # 可以在这里定义__metaclass__，这样只会作用这个类中
    # __metaclass__ = UpperMeta  # python2 
    bar = 'bip'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))
f = Foo()
print(f.BAR)
```

	False
	True
	bip

### django-orm中的object实现
- 从源码中可以发现 Model 的元类指定了 metaclass=ModelBase

```python
class Model(metaclass=ModelBase):

    def __init__(self, *args, **kwargs):
        # Alias some things as locals to avoid repeat global lookups
        cls = self.__class__
        opts = self._meta
        _setattr = setattr
        _DEFERRED = DEFERRED

        pre_init.send(sender=cls, args=args, kwargs=kwargs)
```
- 从ModelBase源码中 `__new__(cls, *args, **kwargs)`中可以发现

```python
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, ModelBase)]
        # 如果没有父类是Model的子类， 那么就普通的创建
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        # 构建新的类属性 new_attrs
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        new_class = super_new(cls, name, bases, new_attrs)
        
        # ....
        new_class._prepare()  # 调用了从 ModelBase 中继承来的_prepare()方法
        new_class._meta.apps.register_model(new_class._meta.app_label,new_class)
        return new_class

```

- 从上述代码可知`__new__`调用了`_prepare`方法

```python
    def _prepare(cls):
        """Create some methods once self._meta has been populated."""
        opts = cls._meta
        # 设置模型的主键
        opts._prepare(cls)
        # ....

        if not opts.managers:
            if any(f.name == 'objects' for f in opts.fields):
                raise ValueError(
                    "Model %s must specify a custom Manager, because it has a "
                    "field named 'objects'." % cls.__name__
                )
            manager = Manager()
            manager.auto_created = True
            cls.add_to_class('objects', manager)
		 # ...

        class_prepared.send(sender=cls)
```

- opts.managers, 将父类管理器都存放到一个列表，如果父类有， 那么将当前Model赋值给管理器，显然如果父类没有管理器，那么，将返回上一步骤，创建`manager = Manager()`, 并通过 `cls.add_to_class()`方法

```python
    @cached_property
    def managers(self):
        managers = []
        seen_managers = set()
        bases = (b for b in self.model.mro() if hasattr(b, '_meta'))
        for depth, base in enumerate(bases):
            for manager in base._meta.local_managers:
                if manager.name in seen_managers:
                    continue

                manager = copy.copy(manager)
                manager.model = self.model  ## 这一步骤很重要
                seen_managers.add(manager.name)
                managers.append((depth, manager.creation_counter, manager))

        return make_immutable_fields_list(
            "managers",
            (m[2] for m in sorted(managers)),
        )
```

- 因为管理器 Manager 有 `contribute_to_class`方法，所以调用了此方法，第一步骤将 Model传给 Manager; 第二步给 Model的object属性赋值到 ManagerDescriptor(self), self代表刚创建的 Manager()对象。而描述符又增加了访问管理器的规则。

```python
   # Model
   def add_to_class(cls, name, value):
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)
            
            
    # Manager        
    def contribute_to_class(self, model, name):
        if not self.name:
            self.name = name
        self.model = model

        setattr(model, name, ManagerDescriptor(self))

        model._meta.add_manager(self)

```

- ManagerDescriptor, 让模型实例无法访问管理器，抽象Model也访问不到， 通过manager_map 映射的名字访问到管理器

```python
class ManagerDescriptor:

    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("Manager isn't accessible via %s instances" % cls.__name__)

        if cls._meta.abstract:
            raise AttributeError("Manager isn't available; %s is abstract" % (
                cls._meta.object_name,
            ))

        if cls._meta.swapped:
            raise AttributeError(
                "Manager isn't available; '%s.%s' has been swapped for '%s'" % (
                    cls._meta.app_label,
                    cls._meta.object_name,
                    cls._meta.swapped,
                )
            )

        return cls._meta.managers_map[self.manager.name]
```

### 依照django-orm 的管理器，去实现sqlalchemy的管理器
> note:
实现的困境主要有两个，一个是讲Model传入到Manager中， 第二个是将db.session数据库会话也传进去，稍后将实现的文档，补充上去

- 实现代码模块 	`ext_sa_manager.py`

```python3
# ext_sa_manager.py

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

    def create(self, **kwargs):
        """创建对象"""
        session = self.session
        if 'id' in kwargs:
            obj = session.query(self.model).get(kwargs['id'])
            if obj:
                return obj
        obj = self.model(**kwargs)
        session.add(obj)
        session.commit()
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


class BaseModel(Model):
    """orm模型基类"""
    # 管理器的默认类
    Manager = None

    objects = None

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}


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
    # return DefineSQLAlchemy
    return rv
```

- 在flask中使用扩展的 sqlalchemy

```python3
from ext_sa_manager import ext_manager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__file__)
db = ext_manager(SQLAlchemy)()
db.init_app(app)
```





