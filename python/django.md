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
