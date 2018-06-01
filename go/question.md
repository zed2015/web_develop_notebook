## 安装 mysql driver 出错
> github.com/go-sql-driver/mysql/utils.go:80: undefined: cloneTLSConfig

### 原因
> ubuntu 安装的go的版本是1.6的, 可用go version 查看， 而mysql驱动要求的版本是1.7及以上，因此产生错误

### 解决办法
> 升级 go的版本

- sudo apt-get remove golang-1.6
- sudo apt-get install golang-1.9
- sudo rm /usr/lib/go-1.6 -rf
- sudo mkdir /usr/lib/go
- sudo cp -r /usr/lib/go-1.9/\* /usr/lib/go/\*
- sudo rm  /usr/bin/go
- sudo ln -s /usr/lib/go/bin/go /usr/bin/go
- go version 
