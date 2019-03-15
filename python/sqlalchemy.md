### flask-sqlalchemy
#### 参数配置
- SQLALCHEMY_COMMIT_ON_TEARDOWN = True, app_context,pop 之前，如果没有异常抛出，会直接进行commit
#### 操作
- 当使用查询时，会开启一个事务,begin
- db.session.add(), 不会进行更新
- db.session.flush(), 会进行更新，但事务不提交
- db.session.commit(),会更新，并且提交事务, 当报错时需要 roll_back，不然会影响一次事务
- db.session.rollback() 会回滚
- db.session.remove(),会roll_back 事务


