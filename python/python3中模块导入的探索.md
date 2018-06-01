## 模块的导入
- 不会重复导入，导入的执行步骤
> 先在 sys.moduels 中查找是否有这个模块，如果有就不会导入，直接使用

```python3
import sys
import logging
print(type(logging))
print(id(logging))
print(id(sys.moduels.get('logging')))
import logging
print(id(logging))
```
输出:

```
<class 'module'>
4524008216
4524008216
4524008216
```
- import 导入与 from ... import ... 导入的区别

```python3
import logging
print(id(logging))
print('从sys.modules中获取到的config是%s'% sys.modules.get('logging.config'))

# from ... import ... 可以用as弄一个别名
from logging import config as cf
# logging里面的config模块
print('config类型%s'% type(logging.config))
# from 从一个包导入一个模块之后，logging 模块增加了一个子属性 config
# 并且 sys.modules 中增加了一个'logging.config'的值，指向了config模块
print(type(logging.config))
print('从sys.modules中获取到的config是%s'% sys.modules.get('logging.config'))
```
输出:

```
4524008216
从sys.modules中获取到的config是None
config类型<class 'module'>
<class 'module'>
从sys.modules中获取到的config是<module 'logging.config' from '/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/logging/config.py'>
```
- 模块与包的导入
- 导入搜索包的路径顺序
	 - python2中在包中的模块导入其他模块的包，会优先从相对本文件的当前路径下查找
	 - python3中则直接在工作目录下查找，如果需要导入相对路径，可以使用 `from .a import A`这种方法

- 函数内的导入
> 从下面的代码可以看出，函数的导入，会将模块实例放到全局的sys.modules中，函数结束后，删除了函数类的Logging变量，只是将引用计数减一，sys.modules中依然还存在logging，

```python3
import sys

def index():
    import logging
    print(id(logging))

index()
try:
    print(logging)
except:
    print('没有这个变量')

print(id(sys.moduels.get('logging')))
```

输出：

```
4520788760
没有这个变量
4520788760
```
- 动态的导入
 
```python
# 动态的导入
# 方法一， 使用 importlib 库（推荐）
import importlib

def test(name):
    m = importlib.import_module(name)
    print(m)
    return m

# 方法二， 使用__import__()函数, __import__是 import语句的内在实现，因为之前说的Python2, python3导入模块，搜索的顺序不一样，导致意外的错误

def test(name):
    m = __import__(name)
    return m
```

- 导入包的重载

> 使用 importlib的reload方法，重载之后，内存地址不变，但是模块的内容变了   
> 模块重载会重新初始化，导致状态丢失    
> 对模块引用有效，但对模块成员引用无法更新， reload不会递归修改成员，所以应避免直接引用其他模块成员，应该通过模块间接访问      

```python3
In [8]: import importlib
   ...:
   ...:
   ...: !echo "x = 666" > demo.py
   ...: import demo
   ...: print(id(demo))
   ...: print(demo.x)
   ...:
   ...: !echo "x = 777" > demo.py
   ...: importlib.reload(demo)
   ...: print(id(demo))
   ...: print(demo.x)
   ...:
4336192312
666
4336192312
777
```
- \_\_all\_\_的作用，与私有变量的_开头的作用

> 在模块中使用这两种方式，仅仅限制 `from A import *`这种导入方式的可导入范围

## logging模块的实现
> 在 flask或者django中往往会涉及到log日志的配置

```python3
# app.py

class LoggerConfig(object):
    """ 日志文件配置"""
    dictConfig = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {'format': '%(asctime)s - %(name)s - %(levelname)s - '
                         '%(message)s - [in %(pathname)s:%(lineno)d]'},
            'short': {'format': '%(message)s'}
        },
        'handlers': {
            # 'smtp': {
            #     'class': 'logging.handlers.SMTPHandler',
            #     'level': 'ERROR',
            #     'formatter': 'email',
            #     'filters': ['email'],
            #     'mailhost': ('example.com', 587),
            #     'fromaddr': 'Mailer <mailer@example.com>',
            #     'toaddrs': ['admins@example.com'],
            #     'subject': 'Application Error',
            #     'credentials': ('mailer@example.com', 'password'),
            #     'secure': ()
            # },
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/flask/cas/web.log',
                'maxBytes': 5000000,
                'backupCount': 10
            },
            'debug': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            },

            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'web': {
                'handlers': ['default'],
                'level': 'DEBUG',
                'propagate': True},
            'werkzeug': {'propagate': True},

            'web.model': {
                'handlers': ['debug'],
                'level': 'DEBUG',
                'propagate': False,
            },

            'web.sqltime': {
                'handlers': ['debug'],
                'level': 'INFO',
                'propagate': False
            }
        },
        # 'root': { 'level': 'DEBUG', 'handlers': ['console'] }
    }
    
from flask import Flask
from logging.config import dictConfig

app = Flask(__name__)
dictConfig(LoggerConfig.dictConfig)  # 1 通过字典中的配置，调用Logging.Logger.manager.getLoger()方法，将logger一个个设置好放在logging.Logger.manager.logerDict 字典中

import views

```

```
# views.py
from app import app
import logging
logger = logging.getLogger() # 2这次导入的logging还是上次导入的那个logging，并从logging.Logger.manager.logerDict字典中根据名字，获取对应的logger即可

@app.route('/')
def index():
	logger.debug('index‘）
	
```

