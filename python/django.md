## python manage.py 操作

- dumpdata 初始数据 

`python manage.py dumpdata app.model -o [file_path]`

-  `loaddata 初始数据 
> 此操作会清空数据库并重新加载数据
> 此操作不会truncate table 只是根据id, update or insert
`python manage.py loaddata [fixtures_path]`

### django 与celery 怎样单元测试
> 当django采用celery做异步任务时，接口测试，会调用异步任务，而异步任务需要celery的worker来执行，难道我测试还要开一个worker吗？肯定会变得很复杂，那么怎么解决呢

- 参考链接 https://stackoverflow.com/questions/4055860/unit-testing-with-django-celery
- 从官方文档中可以看到有一个 CELERY_ALWAYS_EAGER = True， CELERY_EAGER_PROPAGATES_EXCEPTIONS=True参数可以利用

  > 原理就是，会将task.delay(), task.apply_async()变成task.apply()来执行，看源码可以知道。
- 最佳实践的方式
    1. 当异步任务较少时，只针对某个测试需要可以使用装饰器
    ```
    from django.test import TestCase
    from django.test.utils import override_settings
    from myapp.tasks import mytask
    
    class AddTestCase(TestCase):
    
        @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                            CELERY_ALWAYS_EAGER=True,
                            BROKER_BACKEND='memory')
            def test_mytask(self):
                result = mytask.delay()
                self.assertTrue(result.successful())
    
    ```
    - 最简单粗暴的方式就是在settings.py中替换TEST_RUNNER
      `TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'`

      > 源码中很清晰的做了一步，就是将上面两个变量的值设置在配置文件中


### manage.py dumpdata 如何有条件的过滤
> 参考链接 https://stackoverflow.com/questions/8313558/django-selective-dumpdata


### 多个filter与一个filter多个条件的区别
> https://stackoverflow.com/questions/8164675/chaining-multiple-filter-in-django-is-this-a-bug



### django 中间件源码解析

#### 1. 加载中间件

```python3
class WSGIHandler(base.BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_middleware()
        
    def load_middleware(self):
        """
        Populate middleware lists from settings.MIDDLEWARE.

        Must be called after the environment is fixed (see __call__ in subclasses).
        """
        self._view_middleware = []
        self._template_response_middleware = []
        self._exception_middleware = []

        handler = convert_exception_to_response(self._get_response)
        for middleware_path in reversed(settings.MIDDLEWARE):
            middleware = import_string(middleware_path)
            try:
                mw_instance = middleware(handler)
            except MiddlewareNotUsed as exc:
                if settings.DEBUG:
                    if str(exc):
                        logger.debug('MiddlewareNotUsed(%r): %s', middleware_path, exc)
                    else:
                        logger.debug('MiddlewareNotUsed: %r', middleware_path)
                continue

            if mw_instance is None:
                raise ImproperlyConfigured(
                    'Middleware factory %s returned None.' % middleware_path
                )

            if hasattr(mw_instance, 'process_view'):
                self._view_middleware.insert(0, mw_instance.process_view)
            if hasattr(mw_instance, 'process_template_response'):
             	    					self._template_response_middleware.append(mw_instance.process_template_response)
            if hasattr(mw_instance, 'process_exception'):
                self._exception_middleware.append(mw_instance.process_exception)

            handler = convert_exception_to_response(mw_instance)

        # We only assign to this when initialization is complete as it is used
        # as a flag for initialization being complete.
        self._middleware_chain = handler

```

- WSGIHandler `__init__`初始化时调用 `self.load_middleware`方法，增加了 `self._middleware_chain` 属性
- handler是什么
  - mw_instance = middleware(handler)
  - handler = convert_exception_to_response(mw_instance)
  - `self._middleware_chain` = `handler`最终是:
    - mw4.process_request -> mw3.process_request -> mw2.process_request -> mw1.process_request
    - self._get_response
    - mw1.process_response -> mw2.process_responset -> mw3.process_response -> mw4.process_response
    - 每一层都有异常处理成response

#### 2. wsgi 协议调用过程

- WSGIHandler()实例化时加载中间件，返回带有 `__call__`方法的app实例

  ```python3
  def get_wsgi_application():
      """
      The public interface to Django's WSGI support. Return a WSGI callable.
  
      Avoids making django.core.handlers.WSGIHandler a public API, in case the
      internal WSGI implementation changes or moves in the future.
      """
      django.setup(set_prefix=False)
      return WSGIHandler()
  ```

- `__call__`方法如下，按照wsgi协议，接收 environ， start_response 两个参数

```python3
class WSGIHandler(base.BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_middleware()

    def __call__(self, environ, start_response):
        set_script_prefix(get_script_name(environ))
        signals.request_started.send(sender=self.__class__, environ=environ)
        request = self.request_class(environ)
        response = self.get_response(request)

        response._handler_class = self.__class__

        status = '%d %s' % (response.status_code, response.reason_phrase)
        response_headers = list(response.items())
        for c in response.cookies.values():
            response_headers.append(('Set-Cookie', c.output(header='')))
        start_response(status, response_headers)
        if getattr(response, 'file_to_stream', None) is not None and environ.get('wsgi.file_wrapper'):
            response = environ['wsgi.file_wrapper'](response.file_to_stream)
        return response
```

- 看下 `self.get_response`方法

  ```python3
      def get_response(self, request):
          """Return an HttpResponse object for the given HttpRequest."""
          # Setup default url resolver for this thread
          set_urlconf(settings.ROOT_URLCONF)
  
          response = self._middleware_chain(request)
  
          response._closable_objects.append(request)
  
          # If the exception handler returns a TemplateResponse that has not
          # been rendered, force it to be rendered.
          if not getattr(response, 'is_rendered', True) and callable(getattr(response, 'render', None)):
              response = response.render()
  
          if response.status_code >= 400:
              log_response(
                  '%s: %s', response.reason_phrase, request.path,
                  response=response,
                  request=request,
              )
  
          return response
  ```

  - `set_urlconf` 将这次的url配置放到本线程的local中
  - 调用 `_middleware_chain`

  

- `self._get_response`

  ```python3
     def _get_response(self, request):
          """
          Resolve and call the view, then apply view, exception, and
          template_response middleware. This method is everything that happens
          inside the request/response middleware.
          """
          response = None
  
          if hasattr(request, 'urlconf'):
              urlconf = request.urlconf
              set_urlconf(urlconf)
              resolver = get_resolver(urlconf)
          else:
              resolver = get_resolver()
  
          resolver_match = resolver.resolve(request.path_info)
          callback, callback_args, callback_kwargs = resolver_match
          request.resolver_match = resolver_match
  
  #####################important view_middleware###############################
          # Apply view middleware
          for middleware_method in self._view_middleware:
              response = middleware_method(request, callback, callback_args, callback_kwargs)
              if response:
                  break
  
          if response is None:
              wrapped_callback = self.make_view_atomic(callback)
              try:
                  response = wrapped_callback(request, *callback_args, **callback_kwargs)
              except Exception as e:
                  response = self.process_exception_by_middleware(e, request)
  #####################important view_atomic###############################
          # Complain if the view returned None (a common error).
          if response is None:
              if isinstance(callback, types.FunctionType):    # FBV
                  view_name = callback.__name__
              else:                                           # CBV
                  view_name = callback.__class__.__name__ + '.__call__'
  
              raise ValueError(
                  "The view %s.%s didn't return an HttpResponse object. It "
                  "returned None instead." % (callback.__module__, view_name)
              )
  
          # If the response supports deferred rendering, apply template
          # response middleware and then render the response
          elif hasattr(response, 'render') and callable(response.render):
              for middleware_method in self._template_response_middleware:
                  response = middleware_method(request, response)
                  # Complain if the template response middleware returned None (a common error).
                  if response is None:
                      raise ValueError(
                          "%s.process_template_response didn't return an "
                          "HttpResponse object. It returned None instead."
                          % (middleware_method.__self__.__class__.__name__)
                      )
  
              try:
                  response = response.render()
              except Exception as e:
                  response = self.process_exception_by_middleware(e, request)
  
          return response
  ```

  



#### 3. 中间件混合类

```python3
from django.utils.deprecation import MiddlewareMixin

class MiddlewareMixin:
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
```

- 从`__call__`可以看到`response = response or self.get_response(request)`，只要process_request 返回了非空的东西，那么就默认为response，不再进行后续的process_request,以及`get_response`
- 所以 process_request 中间件只能给process_request 增加属性，而不能删除或修改属性，除非很清除知道调用顺序

