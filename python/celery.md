### 重大突破
#### celery worker 接收到任务时， 用的都是同一个Task的实例，即同一个Task()
>测试代码如下，当我调用这个任务时， count变量一次递增
```
class TestAdd(celery_app.Task):
    def run(self, *args, **kwargs):
        if not hasattr(self, 'count'):
            self.count = 1
        else:
            self.count += 1
        logger.debug(self.count)
        return self.count
```

#### celery 任务都过期了
> 时区设置不对
```python
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Etc/UTC'
```

### 捕捉不到 TaskRevokedError 异常
> json 作为序列化手段时, 无法捕捉TaskRevokedError异常，用pickle序列化即可

### class 的__reduce__方法返回的内容，在反序列化时会执行，因此用pickle作为序列化会有攻击
```
class Evil(object):
    def __reduce__(self):
    import os
    return (os.system, ('echo hello',))
```

#### celery sentinel 配置
- celeryconfig.py
```
# broker_url = 'sentinel://10.18.98.12:26377;sentinel://10.18.98.12:26376;sentinel://10.18.98.12:26375'
# broker_transport_options = {'master_name': "redisMaster1"}
# broker_options = {'master_name': "redisMaster1"}
#
# result_backend = 'sentinel://10.18.98.12:26377/0;sentinel://10.18.98.12:26376/0;sentinel://10.18.98.12:26375/0'
# result_backend_transport_options = {'master_name': "redisMaster1"}
```
- flowerconfig.py
```
# broker_url = 'sentinel://{ip}:26377;sentinel://{ip}:26376;sentinel://{ip}:26375'.format(ip=ip)
# BROKER_URL = broker_url
# broker_transport_options = {'master_name': "redisMaster1"}
# broker_options = {'master_name': "redisMaster1"}
```
