# mysql 连接远程主机的方法
>mysql -h 196.168.5.116 -P 3306 -u root -p123456

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

### mysql explain
> https://www.jianshu.com/p/ea3fc71fdc45

### join condition or where condition
> 性能一样,对于inner join 结果一样,对于outer join 结果不一样

### join 链表查询原理
> https://www.cnblogs.com/shengdimaya/p/7123069.html
- 驱动表的选择
    - 优先选择where条件过滤相关的表作为驱动表
    - left 左表
    - 数据量小的表作为驱动表
- 联表算法
    - Index Nested-Loop Join
    - Block Nested-Loop Join
    - Simple Nested-Loop Join


### 改表的AUTO_INCREMENT自曾id
- `ALTER TABLE t2 AUTO_INCREMENT = 10000;`
- 自增id，可以指定，指定一个值之后，AUTO_INCREMENT的值会跟着改变`


### myisam与innoDB
- MyISAM是非事务安全型的，而InnoDB是事务安全型的。
- MyISAM锁的粒度是表级，而InnoDB支持行级锁定。
- MyISAM支持全文索引，而Innodb不支持全文索引
- MyISAM表是保存成文件形式的，在跨平台的数据转移中使用MyISAM存储会省去不少的麻烦。
- InnoDB表比MyISAM表更安全，可以保证数据不丢失的情况下，切换非事务表到事务表



### 事务
- begin
- insert, update, delete
- commit, rollback

### timestamp & datetime
- 默认只能有一个timestamp类型字段, 随着记录修改而修改
- 参考链接 `https://www.cnblogs.com/ivictor/p/5028368.html`
- datetime 字段5.7 版本不能default current_timestamp

### query optimize
- 当查询的结果数据占总数据的0.3以上时，会放弃索引而全表扫描





