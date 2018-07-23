## python manage.py 操作

- dumpdata 初始数据 

`python manage.py dumpdata app.model -o [file_path]`

-  `loaddata 初始数据 
> 此操作会清空数据库并重新加载数据
> 此操作不会truncate table 只是根据id, update or insert
`python manage.py loaddata [fixtures_path]`


