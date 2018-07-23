# *MSA*快速搭建
## 准备工作
### 准备条件
> 安装环境： ubuntu:16.04
>
> 数据库配置:
1. zc@10.0.14.28 作为 master 数据库
2. zc@10.0.14.29 作为 slave 数据库
3. 10.0.14.30 作为虚拟 ip

### mha4mysql 配置原理

> 1. 10.0.14.28 作为 mha4mysql的从节点
> 2. 10.0.14.29 作为 mha4mysql的管理节点

### mysql配置文件位置
因为是用 apt 安装的，所以位置在如下：
> /etc/mysql/mysql.conf.d/mysqld.conf

## master 上配置
###  先在 master 数据库设置虚拟ip
> 有一个深渊巨坑， 一定要带上掩码，否则会出现问题路由转发问题， 导致nginx通信失败
``` bash
sudo ifconfig eth0:1 10.0.14.30/24
```

### 在 master 上创建"dbuser"用户 和 "website"数据库
```mysql
mysql -u root -p
mysql> create database website;
mysql> grant usage on *.* to dbuser@localhost identified by ‘password’;  # 创建数据库的用户, password 自己设定
mysql> grant all privileges on website.* to dbuser@localhost;  # 授权本机使用 "dbuser"登录并拥有 website" 数据库的权限
mysql> grant all privileges on *.* to dbuser@10.0.14.% identified by 'password';  # 授权 "dbuser"用户在 10.0.14.0/24 子网 远程登录 "website" 数据库
mysql> exit
```

### 需要远程主机访问到 master 主机
> 1. 注释掉配置文件的bind_address=127.0.0.1
> 2. `select user, host from user`
> 3. `update user set host='%' where user=root`
### master 数据库配置 
编辑配置文件
> 注释掉配置文件的 `# bind_address=127.0.0.1`,这句话表示mysql 服务只开在本机, 外面无法访问， 因此需要注释掉

```
server-id=1
log_bin = /var/log/mysql/mysql-bin.log  # 设置二进制日志文件存储的位置
expire_logs_days = 7  # 避免大量的日志文件占用内存，保存七天的日志即可
binlog_do_db = website  # 设置需要保存二进制日志文件的数据库
```

```bash
/etc/init.d/mysql restart  # 重启数据库
sudo systemctl restart mysql.service  # 如果是apt安装的可以用此方法重启
```
### 在 master 上创建"salve_user"用户, slave 用此用户进行复制
```mysql
mysql -u root -p
mysql> grant REPLICATION SLAVE on *.* to 'slave_user'@'%' IDENTIFIED BY 'password';
mysql> flush privileges  # 生效上一步做的更改
mysql> show master status  # 记住Postion的位置如154 稍后将用到这个数据
mysql> exit
```


## salve 上配置
### 在 slave 上创建"dbuser"用户 和 "website"数据库
```mysql
mysql -u root -p
mysql> create database website;
mysql> grant usage on *.* to dbuser@localhost identified by ‘password’;  # 创建数据库的用户, password 自己设定 保证和master 上的密码一致
mysql> grant all privileges on website.* to dbuser@localhost;  # 授权本机使用 "dbuser"登录并拥有 website" 数据库的权限
mysql> grant all privileges on *.* to dbuser@10.0.14.% identified by 'password';  # 授权 "dbuser"用户在 10.0.14.0/24 子网 远程登录 "website" 数据库
mysql> exit
```

### slave 数据库配置 
编辑配置文件
> 注释掉配置文件的 `# bind_address=127.0.0.1`,这句话表示mysql 服务只开在本机, 外面无法访问， 因此需要注释掉

```
server-id=2
log_bin = /var/log/mysql/mysql-bin.log  # 设置二进制日志文件存储的位置
expire_logs_days = 7  # 避免大量的日志文件占用内存，保存七天的日志即可
binlog_do_db = website  # 设置需要保存二进制日志文件的数据库
relay-log = /var/log/mysql/mysql-relay-bin.log  # slave 服务器将 master服务器上的log-bin文件拷贝到这个文件， 并执行这个文件里的数据库操作  称为中继日志
relay_log_space_limit=2G
```

```bash
/etc/init.d/mysql restart  # 重启数据库
sudo systemctl restart mysql.service  # 如果是apt安装的可以用此方法重启
```

### 在 slave 上开启跟随 master 的slave 模式
```mysql
mysql> change master to master_host='10.0.14.28', master_user='slave_user', master_password='123456', master_log_file='mysql-bin.000001', master_log_pos=154
mysql> start slave;
mysql> show slave status\G;   # 查看slave 开启状态， slave_io_running & salve_sql_running 如果为yes 说明开启成功
```
>
> `nohup masterha_manager --conf=/etc/masterha/app1.cnf < /dev/null > /var/log/masterha/app1/app1.log 2>&1 &`

## MHA 配置
> ### 在两个服务器上安装 MHA Node 及额外的库
1. 在[mha4mysql](https://github.com/yoshinorim/mha4mysql-manager) 的官网github地址下载.tar.gz 版本的节点，以及管理节点 
2. 解压mha4mysql-node-0.56.tar.gz;
3. 执行下列命令:
```bash
sudo apt install libdbd-mysql-perl
cd mha4mysql-node-0.56
perl Makefile.PL
make
sudo make install
```
> ### 在slave 上安装 MHA Manager 及额外的库
1. 在[mha4mysql](https://github.com/yoshinorim/mha4mysql-manager) 的官网github地址下载.tar.gz 版本的节点，以及管理节点 
2. 解压mha4mysql-manager-0.56.tar.gz;
3. 执行下列命令:
```bash
sudo apt install libdbd-mysql-perl
sudo apt-get install libconfig-tiny-perl
sudo apt-get install liblog-dispatch-perl
sudo apt-get install libparallel-forkmanager-perl
cd mha4mysql-manager-0.56
perl Makefile.PL
make
sudo make install
```
4. 创建MHA配置文件
* 应用配置
> `vim /etc/msterha/app1.cnf`

> 配置如下:

 ```
 [server default]
 user=mhauser
 password=123456
# working directory on the manager
 manager_workdir=/var/log/masterha/app1
# manager log file
 manager_log=/var/log/masterha/app1/app1.log
# working directory on MySQL servers
 remote_workdir=/var/log/masterha/app1

 [server1]
 hostname=10.0.14.28

 [server2]
 hostname=10.0.14.29
```
* 全局配置
> `vim /etc/masterha_default.cnf`
> 配置如下:

 ```
[server default]
user=mhauser
password=123456
ssh_user=cmgos
master_binlog_dir= /var/log/mysql
remote_workdir=/data/log/masterha
#secondary_check_script= masterha_secondary_check -s remote_host1 -s remote_host2
ping_interval=3
master_ip_failover_script=/script/masterha/master_ip_failover
#shutdown_script= /script/masterha/power_manager
#report_script= /script/masterha/send_master_failover_mail
```

5. 在两个数据库上创建被MHA 使用的 ‘mhauser’ 
```
sql -u root -p
mysql> grant all on *.* to 'mhauser'@'10.0.14.%'  identified by 'password';
mysql> flush privileges

```
6. 创建 “master_ip_failover” 脚本
`vim /script/masterha/master_ip_failover`
内容如下：[点击这里](https://github.com/zed2015/mha4mysql/blob/master/master_ip_failover)
注意修改 文件权限为你搭建 mha 用户 并 chmod +x

### 构建互相信任，免密码登录ssh

### 测试配置是否正确
* 检测 SSH 配置
`masterha_check_ssh --conf=/etc/masterha/app1.cnf`
* 检测 主从复制配置
`masterha_check_repl --conf=/etc/masterha/app1.cnf`
如果有问题， 分析日志， 一步一步排查, 常见问题见下面问题

### 后台启动 MHA
`nohup masterha_manager --conf=/etc/masterha/app1.cnf < /dev/null > /var/log/masterha/app1/app1.log 2>&1 &`
检查状态
`masterha_check_status --conf=/etc/masterha/app1.cnf`

# [参考博客](http://www.arborisoft.com/how-to-configure-mysql-masterslave-replication-with-mha-automatic-failover/)


## 问题
> 1. 期间遇到权限问题， 请通过 `usermod -a -G [group] username`, `chown`, `chomod` 更改权限，建立文件夹 

> 2. Slave failed to initialize relay log info structure from the repository ,解决方案 stop salve; reset slave all; reset master;

> 3. 5.22 版本的perl 会遇到 redundant argument  in sprintf 错误，解决方案 按照github上的[修复](https://github.com/yoshinorim/mha4mysql-node/pull/23/files?diff=split)更改两处代码既可以, 需要用到root权限

> 4. MHA 代码现已经在 github上托管了， [mha4mysql-node](https://github.com/yoshinorim/mha4mysql-node)
> [mhasmysql-manager](https://github.com/yoshinorim/mha4mysql-manager)

> 5. 缺少包 `sudo apt-get install libswitch-perl`

#### ssh 远程执行sudo 命令设置
1. 在 /etc/sudoers 最后一行 添加 
  `username ALL = NOPASSWD: /usr/sbin/ifconfig`
2. ssh -t username@ip "sudo cmd"
