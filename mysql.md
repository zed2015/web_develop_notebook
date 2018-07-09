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




