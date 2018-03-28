## python 基础知识

+++++

### 1. os.environ,以及系统环境变量 

+ 环境变量的层级分为四个层级 
  1. /etc/profile
  2. ~/.bashrc
  3. export key=value
  4. python 中 os.environ.setdefault(key, default), os.environ.get(), os.environ.pop()
+ os.environ 是一个系统环境变量的映射字典， 在 import os 初次导入时， 就获取系统的变量， 中途通过export 导入的不能获取
+ os.environ.setdefault(key, default) 如果有这个系统变量，那么返回value， 如果没有就设置default到os.environ
+ os.environ 并没有真的改变系统变量， 只是改变了os.environ 这个字典， 在其他进程也获取不到， 无法在外面获取， echo  $ var 无法获取





