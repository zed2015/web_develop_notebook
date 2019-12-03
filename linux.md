### 参考链接https://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html
## 更改用户名的uid与gid
```
usermod -u uid username
groupmod -g gid groupname

```
## SSH 操作 
- 生成ssh钥匙, 指定密码
`ssh-keygen -f ~/.ssh/id_rsa_spc -p'123456'`

- 上传公钥匙到远程机器的authorized_keys里
`ssh-copy-id -i /home/zc/.ssh/id_rsa.pub root@ip`

- 指定特定的私密钥匙进行认证
`ssh -i ~/.ssh/id_rsa_spec root@ip`

- 代理的使用
    - `ssh-agent bash`
    - `ssh-add ~/.ssh/id_rsa_spec`
    - `ssh-add -l[-L]`

## 批量命名
`rename -s/htm/html/ ./*`


## linux 启动顺序
1. /etc/rc.local
> 很多环境变量可能没有设置，因此需要用绝对路径

## 如何查看ubuntu的详细版本
- `sudo lsb_release -a `
- `cat /etc/issue`

## tree 命令生成文本文件结构

- `tree -I '*pyc|ansible' -U -L 2 -v --dirsfirst  -n -o workdir_L2.txt`

## wc ls作何统计文件个数

- `ls -lR | grep "^-" |wc -l`
> -R 循环递归
- `ls -lR | grep "^d" |wc -l`
- `ls -l | grep "^d" |wc -l`
- `ls -l | grep "^d" |wc -l`

## zip 压缩命令
- zip -r dest.zip dest/ -x dest/.git/\*
- zip -r faceEngineApi.zip faceEngineApi/ -x faceEngineApi/.git/\* \*.pyc faceEngineApi/test/\*


## sudo 命令会忽视environment
- sudo -E
- https://stackoverflow.com/questions/8633461/how-to-keep-environment-variables-when-using-sudo

## sudo no password
>https://askubuntu.com/questions/192050/how-to-run-sudo-command-with-no-password

## rsync
 - `rsync -avt dest_dir user@ip:/dir/`

## cut 命令
> https://www.geeksforgeeks.org/cut-command-linux-examples/
- `cut -d: -f1 filename |sort

## ubuntu不能支持中文
- sudo locale-gen zh_CN.UTF-8
- sudo update-locale LANG=zh_CN.UTF-8
- sudo vim /etc/default/locale 
    - LC_ALL="zh_CN.UTF-8"
    - LANGUAGE="zh_CN.zh"
- locale charmap

## grep -
- `grep '\-\-\-' your_file`

### 用户相关操作
> https://www.jianshu.com/p/f468e02f38a0

### 查看代码行数
- `find . -name '*.php' | xargs wc -l`

### 动态连接库管理ldconfig
> `https://blog.csdn.net/u011636567/article/details/77162217`

### 查看nds
- cat /etc/resolv.conf
- nmcli dev show |grep DNS

### 虚拟网络
> `https://blog.csdn.net/phunxm/article/details/9498829`
> `https://www.ibm.com/developerworks/cn/linux/1310_xiawc_networkdevice/`

### shadowsock 代理
> `https://laucyun.com/5cce9d01b0a0210482d65f5bc040d83b.html`, `https://www.polarxiong.com/archives/Ubuntu-16-04%E4%B8%8BShadowsocks%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%AB%AF%E5%AE%89%E8%A3%85%E5%8F%8A%E4%BC%98%E5%8C%96.html`
- shell 配置
  - export http_proxy=http://127.0.0.1:8118
  - export https_proxy=http://127.0.0.1:8118
  - export ftp_proxy=http://127.0.0.1:8118

### 查看磁盘带宽
> `dd if=/dev/zero of=/mnt/test/rnd2 count=1000000`

### watch 命令
> `watch -n 1 -d nvidia-smi`

### 固定修改网卡名字
> `https://askubuntu.com/questions/1158443/rename-interface-permanently`

### 查看文件夹子大小
> `du -h - max-depth=1`

### 磁盘分区，文件系统挂载
- 磁盘分区
    - 查看详情 `fdisk -l` 
    - 磁盘可以建立主分区，扩展分区，扩展分区可以建立逻辑分区
    - 查看分区挂载详情 `df -h`
- 分区格式化类别 `mkfs.ext2 ext3 ext4 partition`,234属于文件系统类型，不断优化的文件系统
- 挂载
    - mount partition dst-dir
    - vim /etc/fstab

    
### 查看信号相关
- man 7 signal
- kill -l 查看所有信号
- python 信号注册函数，不是在内核中;

### scp 免输入密码
>`sshpass -f "/path/to/passwordfile" scp -r user@example.com:/some/remote/path /some/local/path`

### nvidia-docker
> `https://blog.csdn.net/junxiacaocao/article/details/79471770`
