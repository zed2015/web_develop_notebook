### __call__的使用
- 我们知道类的实例通过()调用时，会调用__call__方法
- 而类是元类的实例,class()调用时，会调用元类的__call__方法
- 元类的__call__方法调用类的__new__方法，在调用类__init__方法返回出一个实例对象

### 元类来做单例模式代码
```python3
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
```
