# mysql 连接远程主机的方法
>mysql -h 192.168.5.116 -P 3306 -u root -p123456

# 导出数据
> mysqldump -uroot -p > xxx.sql

# 导入数据
> mysql -h localhost -uroot -p database_name < data.sql

> pg_dump -h localhost -U postgres -d vps_news > vps_news.sql

# 忘记root密码解决方法
> 1. 进入配置文件加入 `skip-grant-tables`
> 2. 重启msyql, `sudo service mysql restart`
> 3. 进入mysql,修改密码 `update mysql.user set authentication_string=password('123456') where user=root and host='localhost'`
> 4. 重启msyql ,用新密码进入即可

# 修改表的外键约束

- 删除约束
`alter table table_name drop foreign key constraint_name`
- 添加约束
alter table table_name add constraint constraint_name foregin key (`user_id`) references `other_table` (`id`);


## 查询
### datetime字段查询
- mysql 中 datetime 字段可以使用like查询
- django中的datetime查询不支持like
- django中支持startswith 查询 


## mysql drop truncate 很慢的解决办法
- 重新启动mysql服务
- 方法2
    - `rename table table_name to t1`
    - `create table table_name like t1`
    - `drop table t1`

- 方法3
    - `SELECT TABLE_NAME,TABLE_ROWS,DATA_LENGTH FROM TABLES WHERE TABLE_SCHEMA='mydatabase' AND TABLE_NAME='mytable'`
    - `show processlist;`
    - `kill id`





