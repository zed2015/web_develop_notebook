# flask 学习，常见总结
> note:
因flask作为微小框架， 有很好的设计哲学，个人也从django转向flask 并使用py3开发新的项目， 对于遇到的问题，会记录在此文章中，以便后续的学习，交流

## 常见问题（采坑记录）
### falsk与db交互的问题

#### mysql
- 因py3不再支持 mysqldb >> mysql-python
    - pip install mysql-python 会报错
    - pip install pymysql
    - export SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:passwd@ip:3306/database_name

####  sqlalchemy datetime create update
> https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    - sqlalchemy 设置数据库默认 server_default 实现datetime字段精确到毫秒的方案
    > https://stackoverflow.com/questions/47458722/how-to-database-side-declare-default-high-precision-datetime-default-onupdate
        - # # create_time = db.Column(DATETIME(fsp=6), nullable=False, server_default=text('CURRENT_TIMESTAMP(6)'), doc='创建时间')
#### is\_delete 字段的默认过滤
- how to filter is_delete =true
- https://stackoverflow.com/questions/40193259/how-to-implement-a-default-condition-in-all-sqlalchemys-queries
- https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-isqlalchemy

#### sqlalchemy bulk create
- https://stackoverflow.com/questions/25694234/bulk-update-in-sqlalchemy-core-using-where

#### query update
- # https://stackoverflow.com/questions/33703070/using-sqlalchemy-result-set-for-update
- # synchronize_session = False
- # https://docs.sqlalchemy.org/en/rel_1_0/orm/query.html?highlight=update#sqlalchemy.orm.query.Query.update
- 如下
```
# mappings = [{'id': id, 'status': Sku.SkuStatus.is_deal.value} for id in sku_ids]
# logger.debug(mappings)
# db.session.bulk_update_mappings(Sku, mappings)
# table = Sku.__table__
# sql = table.update().where(table.c.status == Sku.SkuStatus.supplement.value).\
#     value(status=Sku.SkuStatus.is_deal)
# db.engine.execute(sql)
```

#### exist
```
# query = db.session.query(Sku.query.filter(Sku.status == Sku.SkuStatus.is_deal).exists())
# has_dealing = query.scalar()
```
#### bulk insert
```
# 批量操作, 注意捕捉错误异常
# try:
#     db.engine.execute(Sku.__table__.insert(), sku_info_list)
# except Exception as exc:
#     logger.error(exc)
#     return {'message': six.text_type(exc)}, 400
# return {'message': 'success create'}

```

#### 测试时，truncate table
```
def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print 'Clear table %s' % table
        session.execute(table.delete())
    session.commit()
```


