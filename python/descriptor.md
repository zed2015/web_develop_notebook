# cas 后端开发说明
----
### python高级知识
#### 描述符
- 描述符号的作用
    - 设置属性的时候做些检测的处理
    - 缓存
    - 设置属性不能被删除
    - 设置只读的属性
    - 属性更改的判断检测
- 描述符的说明
    - 描述符是对象属性的代理
    - 将某种特殊类型的类的实例指派给一个`类`的属性
    - 特殊类型实现了`__get__, __set__, __delete__`方法
    - 只实现了 `__get__`称为非数据描述付， 实现了两种方法的称为数据描述符
    _ `__getattribute__`方法无条件调用
      > note:class.x 》class.__dict['x'].__get__(None, class)
- python中访问属性的优先级别
    - `__getattribute__(self,name)`
    - 数据描述符
    - 实例属性
    - 类属性/非数据描述符
    - `__getattr__`
    

---
### flask abort(status, *args, **kw) 函数源码解析
- Aborter()(status, *args, **kw)
```python

class Aborter(object):

    """
    When passed a dict of code -> exception items it can be used as
    callable that raises exceptions.  If the first argument to the
    callable is an integer it will be looked up in the mapping, if it's
    a WSGI application it will be raised in a proxy exception.

    The rest of the arguments are forwarded to the exception constructor.
    """

    def __init__(self, mapping=None, extra=None):
        if mapping is None:
            mapping = default_exceptions
        self.mapping = dict(mapping)
        if extra is not None:
            self.mapping.update(extra)

    def __call__(self, code, *args, **kwargs):
        if not args and not kwargs and not isinstance(code, integer_types):
            raise HTTPException(response=code)
        if code not in self.mapping:
            raise LookupError('no exception for %r' % code)
        raise self.mapping[code](*args, **kwargs)
```
- defualt_exception是一个字典{400: HttpException}
```python

def _find_exceptions():
    for name, obj in iteritems(globals()):
        try:
            is_http_exception = issubclass(obj, HTTPException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.code is None:
            continue
        __all__.append(obj.__name__)
        old_obj = default_exceptions.get(obj.code, None)
        if old_obj is not None and issubclass(obj, old_obj):
            continue
        default_exceptions[obj.code] = obj
_find_exceptions()
del _find_exceptions
```

- 如果 abort(response), 那么其结果是raise HTTPException(response)
    - 在下面代码中又重新返回响应
    ```python
    
    def handle_http_exception(self, e):
        """Handles an HTTP exception.  By default this will invoke the
        registered error handlers and fall back to returning the
        exception as response.

        .. versionadded:: 0.3
        """
        # Proxy exceptions don't have error codes.  We want to always return
        # those unchanged as errors
        if e.code is None:
            return e

    ```


---
### sqlalchemy 源码解析
- db.Model
    - self.make_declarative_base(model_class, metadata)
      > model_class = Model, metadata = None
    
    ```python
    
    if not isinstance(model, DeclarativeMeta):
        model = declarative_base(
            cls=model,
            name='Model',
            metadata=metadata,
            metaclass=DefaultMeta
        )
    
    if not getattr(model, 'query_class', None):
        model.query_class = self.Query  # BaseQuery

    model.query = _QueryProperty(self)
    return model
    ```
    - model.query 是一个描述符
    ```python
    
    class _QueryProperty(object):
        def __init__(self, sa):
            self.sa = sa

        def __get__(self, obj, type):
            # type = Model
            try:
                mapper = orm.class_mapper(type)
                if mapper:
                    return type.query_class(mapper, session=self.sa.session())
            except UnmappedClassError:
                return None

    ```
    - declarative_base()
    ```python
    class DeclarativeMeta(type):
        def __init__(cls, classname, bases, dict_):
            if '_decl_class_registry' not in cls.__dict__:
                _as_declarative(cls, classname, cls.__dict__)
            type.__init__(cls, classname, bases, dict_)

        def __setattr__(cls, key, value):
            _add_attribute(cls, key, value)
        
    ```
    
    - classdict
    ```python
    
    class_dict = dict(_decl_class_registry=class_registry,
                      metadata=lcl_metadata)

    if isinstance(cls, type):
        class_dict['__doc__'] = cls.__doc__

    if constructor:
        class_dict['__init__'] = constructor
    if mapper:
        class_dict['__mapper_cls__'] = mapper
    ```
    
    - 结果是Model的子类, 含有 classdict中的类属性
   

### 三方扩展说明
  > note:
三方扩展位置统一放在 ./ext.py中

- flask-babel
  > note: 用来本地化用户语言，用户时区的一个包
    - flask_babel.datetime_formatter()
    - @babel.localeselector
    - @babel.timezoneselector
 
- flask-session
  > note: flask 默认的 client side session,
  现在需要使用服务器端 session， 使用redis
  -  werkzeug.datastructures.CallbackDict
      > 作为session改变的核心，更新回调，实现很棒，可以借鉴学习
  ```python
  from werkzeug.datastructures import CallbackDict
  class Dict(CallbackDict):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified=False
   
  ```
  - 签名用的是 `itsdangerous.Siner`
  - flask留出来的session接口为 继承`from flask.sessions import SessionInterface, SessionMixin`
 
- flask-rest-jsonapi
    > jsonapi
    - Resource
        - view_func
        
    - DataLayer
        - get_collection
        - create_object
        - get_object, retrieve_object
        - update_object
        - delete_object
        
    - QSManager
        - filter
        - sort
    - Schema
        - dump
        > serialize object to dict
             
            - MarshalResult
        - load
        > deserializer data to object
        
            - UnMarshalResult
    
    
    
    
   

  
  




