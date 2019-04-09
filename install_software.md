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
### install opencv java in mac
> `https://opencv-java-tutorials.readthedocs.io/en/latest/01-installing-opencv-for-java.html`
### cuda9.2 的安装
- cuda9.2 依赖 nvidia driver 396 以上
    - 卸载低版本的nvidia驱动
    > `sudo apt-get purge nvidia*`
    - 换源
    > `sudo add-apt-repository ppa:graphics-drivers, sudo apt-get update`
    - 查找显卡驱动最新版本
    > `sudo apt-cache search nvidia`
    - apt 安装
    > `sudo apt-get install nvidia-396 nvidia-settings nvidia-prime`
    - 重启电脑,一定要做
    - 验证是否安装成功
    > `lsmod | grep nvidia 有输出`， `lsmod | grep nouveau` 无输出
    - 停止自动更新
    > `sudo apt-mark hold nvidia-396`

- 安装 cuda9.2
    - 从官网下载 `cuda_9.2.148_396.37_linux.run`
    - 安装 `sudo sh cuda_9.2.148_396.37_linux.run`
    - 交互界面，有一项是否安装驱动，选择否
