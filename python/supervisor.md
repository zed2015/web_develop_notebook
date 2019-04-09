# python2.7 的supervisor 启动uwsgi,print中文会报错
- environment=LC\_ALL='en\_US.UTF-8',LANG='en\_US.UTF-8'
```
env = LANG="en_US.UTF-8"
env = LANGUAGE="en_US.UTF-8"
env = PYTHONIOENCODING=UTF-8
```
