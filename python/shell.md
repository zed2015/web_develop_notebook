
### 解压打包的pyton命令
shutils.make_archive(base_name, format, root_dir, base_dir)
- base_name 目标文件路径，不包含打包的后缀名 
- format 格式 zip, tar.gz
- root_dir 切换到哪个文件夹作为工作路径进行打包操作，一般切换到需要打包的文件夹所在的目录, 默认为工作路径
- base_dir 打包的文件夹，一般填相对于root_dir 的相对路径，默认为工作路径


