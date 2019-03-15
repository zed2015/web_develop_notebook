## goland 的安装方法

- 去官网下载最新的goland安装包
- http://idea.youbbs.org
> 可以激活该软件

## ubuntu 16.04 安装deb包
- dpkg 安装
    1 sudo dpkg -i youdao.deb
    - sudo apt install -f 
    - sudo dpkg -i youdao.deb
- gdebi 包管理器安装
    1. sudo gdebi youdao.deb

## 安装typora
```sh
# or run:
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA300B7755AFCFAE
wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -
# add Typora's repository
sudo add-apt-repository 'deb https://typora.io/linux ./'
sudo apt-get update
# install typora
sudo apt-get install typora
```
### 安装java 建立软连接
```
$ JAVA_HOME=/usr/java/jdk1.8.0_05/
$ sudo update-alternatives --install /usr/bin/java java ${JAVA_HOME%*/}/bin/java 20000
$ sudo update-alternatives --install /usr/bin/javac javac ${JAVA_HOME%*/}/bin/javac 20000
update-alternatives --config java
```
