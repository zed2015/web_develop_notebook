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

