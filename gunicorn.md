# gunicorn 源码阅读笔记

## 一、gunicorn 启动命令解析
> note:源码如下

```python
# -*- coding: utf-8 -*-
import re
import sys

from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run())
```
### 1、总结
从源码中可以看出是调用 gunicorn.app.wsgiapp.run

## 二、执行流程

- gunicorn.app.wsgiapp:WSGIApplication().run()
    - self.do_load_config()
      > 加载配置类到 self.cfg


- gunicorn.arbiter:Arbiter(WSGIApplication()).run
    1. self.__init__()
        - self.setup(app)
            - self.app.wsgi()
              > 导入wsgi_app实例对象
        - self.START_CTX = {args,cwd,0}

- self.run()
    - self.start()
      > 做一些准备工作
    - self.manage_worker()
      > 管理进程
        - self.spawn_workers() # 扩展进程数
            - self.worker_class() >> self.cfg.worker_class
            - gunicorn.workers.gthread.ThreadWorker

    


