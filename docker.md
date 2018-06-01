
### 镜像命令
> docker image ls

> -f 为过滤 docker image ls -f dangling=true

> docker image prume

> docker image rm [dest]

> docker image rm $(docker image ls -q redis)

> #### use dockerfile build image

>> docker build -t nginx:v2 .   # (.) 是上下文路径

### 容器命令
* docker run -i -t [-d守护进程运行]  ubuntu:16.04 /bin/bash
* docker run -d -P
    --name
    --mount type=bind, source=[s], target=[t]  # 可以在dockefile中事先指定
    python app.py

* docer container start
* docker container ls
* docker container logs [container ID or NAMES]
* docker container ls -a
* docker container start [container]
* docker container restart [container]
* docker exc -it [container ID] bash
* docker container rm[-f]
* docker contianer prune  # 删除所有中止的容器
* docker export containerid * ubuntu.tar
* cat ubuntu.tar | docker import - test/ubuntu:v1.0
* docker inspect web

### 仓库命令
* docker login
* docker logout
* curl 127.0.0.1:5000/v2/catalog  # 查看私有仓库

### 数据管理
* docker volume create my-vol
* docker volume ls
* docker volume inspect my-vol
* docker volume rm my-vol
* docker volume prune


### 网络管理
* docker port container_name port

### 容器互联
* docker network create -d bridge my-net
* docker run -it --rm --name busybox1 --network my-net busybox sh
* docker run -it --rm --name busybox2 --network my-net busybox sh

### dockerfile 指定
* unbuild  # 是为了构建下一层镜像的命令

* workdir  # 改变以后各层的工作目录
* USER   # 改变以后各层的默认用户 gosu

* copy [source, dest]  # 同add
* CMD ["nginx", "-g", "daemon off;"]  # 容器启动命令
* ENTRYPOINT [ "curl", "-s", "http://ip.cn" ]
* ENV VERSION=1.0 DEBUG=on \
    NAME="Happy Feet"  # ENV key value

* ARG <参数名*[=<默认值*]  # 构建环境的环境的变量， 不是运行命令的环境变量
* VOLUME ["<路径1*", "<路径2*"...]  # 可以事先挂在目录为匿名卷
* EXPOSE <端口1* [<端口2*...]  #  申明容器是用什么端口

### compose 命令
* docker-compose build [options] [service] --force-rm --no-cache --pull

* docker-compose config

* down  up
     > docker-compose up [options] [service...] [-d守护] [--no-deps]

* exec

* images

* docker-compose kill -s sigint

* docker-compose logs [options] [service...]

* docker-compose pause | unpause [service...]

* docker-compose port [options] service private_port --protocol=proto --index=index

* docker-compose ps [-q]

* pull push

* start, stop,restart

* rm -v

* docker-compose run ubuntu ping docker.com  # 在指定的服务上执行一个名利将嗯

* docker-compose scale web=3 db=2

* top

### compose 模板文件
* build | image
     context
     dockerfile
     args
     cache_from
     cap_add: - ALL | cap_drop; - NET_ADMIN
     command

* depends_on

* extra_hosts

* helthcheck

* loggin

    > driver:syslog

    > options:1








