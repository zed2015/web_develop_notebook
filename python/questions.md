## 安装缺包问题

### MySQL-python 依赖的包安装
> `sudo apt-get -y install libmysqlclient-dev`

### Python-ldap 依赖的包安装
> `sudo apt-get -y install libsasl2-dev python-dev libldap2-dev libssl-dev`

### 安装gevent 出错
> `apt-get install libevent-dev`


## 重要的细节

### djang orm中的 iexact 与 exact，无效
- 因为如果数据库中默认的 collate utf8_general_ci 的时候，都是大小写不敏感的
- 解决办法
    - `select * where binary name='zhangchi'`
    - `User.objects.extra(where=['binary name=%s'], params=[username])`
    - `alter table user change name name varchar(128) character set utf8 collate utf8_bin`
    - 或者创建表及数据库之前， 指定collate utf_bin
    - `alter table user default character set utf8 collate utf8_bin`
    - `alter database d_name default character set utf8 collcate utf8_bin`
- 如果数据库本身大小写不敏感，那么 = 以及exact 都是不敏感的
