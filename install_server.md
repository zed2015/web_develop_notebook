### ubuntu 安装redis
```bash
sudo apt update
sudo apt install redis-server
```
### ubuntu 安装nginx
```bash
sudo apt update
sudo apt install nginx
```
### install kafka
> `https://hevodata.com/blog/how-to-install-kafka-on-ubuntu/`

### ubuntu 安装 python 虚拟环境包管理工具
```bash
> sudo apt install python-pip
> sudo pip install virtualenv
> sudo pip install virtualenvwrapper
> sudo easy_install virtualenvwrapper
> mkdir ~/.virtualenvs
在~/.bashrc 中添加：
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
> source ~/.bashrc
```

### ubuntu 安装 NFS 服务器与客户端
#### 服务器端

1. 安装服务
    sudo apt install nfs-kernel-server
-  编写配置文件

    sudo vim /etc/exports
    > /data *(rw,sync,no_subtree_check,no_root_squash)
- 创建目录
    sudo mkdir -p /data 
- 重启nfs服务
    sudo service nfs-kernel-server restart
- 常用命令工具
    - 显示已经mount到本机nfs目录的客户端机器
        sudo showmount -e localhost
    - 将配置文件中的目录全部重新export 一次！ 无需重启服务
        sudo exportfs -rv
    - 查看nfs的运行状态
        sudo nfsstat
    - 查看rpc执行信息
        sudo rpcinfo
#### 客户端

1. 安装客户端工具
    sudo apt install nfs-common
-  查看nfs服务器上的共享目录
    sudo showmount -e 10.0.99.243
-  创建本地挂在目录
-  **挂在共享目录**
    sudo mount -t nfs 10.0.99.243:/data /mnt/data

    









