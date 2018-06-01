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

### 2. 包的安装
- pip install html-TestRunner

### 3. python3.6的安装
> ubuntu 默认的python3版本是python3.5，很多系统需要的是依赖这个包，所以不能删除，只能再额外安装python3.6

```shell
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz
tar -xvf Python-3.6.2.tar.xz
cd Python-3.6.2
 ./configure --prefix=/usr/local/lib/python3.6
sudo make
sudo make install
#sudo mv /usr/bin/python3.6 /usr/local/lib/
# 默认是安装到 /usr/local/lib/python3.6/bin/python3.6 所以需要建立一个软链接
sudo ln -s /usr/loca/lib/python3.6/bin/python3.6 /usr/bin/python3.6
```




