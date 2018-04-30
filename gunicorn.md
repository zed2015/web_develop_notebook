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

        - self.LISTENERS = [] = sock.create_socket(self.cfg,self.log, self.fds)
          > 创建套接字

            - self.sockets = socket.formfd()
    - self.manage_worker()
      > 管理进程

        - self.spawn_workers()
        - self.spawn_worker() # 扩展进程数
            - self.worker_class() >> self.cfg.worker_class
            - gunicorn.workers.gthread.ThreadWorker
        - worker.init_process()  # 子进程worker 初始化 

            - self.poller = selectors.DefaultSelector()
            - self.init_signals()
            - self.load_wsgi() >> self.wsgi = self.app.wsgi() = flask_app
            -self.run()  # while loop, 真正的进程死循环接受套接字链接
    - while True:
      > 死循环来根据子进程状态进行kill，spawn进程，保证进程数量o

        - self.murder_workers()
        - self.spawn_workers()


- worker.run()
  > 子进程跑起来了

    - self.poller = gunicorn.selectors.epool()
    - while True:
        - self.pooler.register(sock, event, callback=self.accept)
        - self.poller.poll() >> self.callback()
        - self.accept(server_name, listener)
            ```python 
            sock, client = listener.accept()
            # initialize the connection object
            conn = TConn(self.cfg, sock, client, server) # 参数容器
            self.nr_conns += 1
            # enqueue the job
            self.enqueue_req(conn)
            ```
            ```python
            def enqueue_req(self, conn):
                conn.init()
                # submit the connection to a worker
                fs = self.tpool.submit(self.handle, conn) # 将任务丢进线程池中
                self._wrap_future(fs, conn) # 将fs 任务进行包装，添加回掉函数
            ```
            - self.handle()
            - self.handle_request()
            - self.wsgi()
            - self.finish_request()
            


