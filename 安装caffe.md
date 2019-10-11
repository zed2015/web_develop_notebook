### 1. 安装caffe



### 编译安装 jsoncpp

``` shell
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=release -DBUILD_STATIC_LIBS=ON -DBUILD_SHARED_LIBS=OFF  -DARCHIVE_INSTALL_DIR=. -G "Unix Makefiles" ..
make
```

### 升级cmake

- Check your current version with `cmake --version`
- Uninstall it with `sudo apt remove cmake`
  Visit https://cmake.org/download/ and download the latest binaries
  In my case cmake-3.6.2-Linux-x86_64.sh is sufficient copy the binary to `/opt/`
- `chmod +x /opt/cmake-3.*your_version*.sh` (chmod makes the script executable)
- `sudo bash /opt/cmake-3.*your_version.sh` (you'll need to press y twice)
- The script installs to /opt/cmake-3.*your_version* so in order to get the cmake command, make a symbolic link: `sudo ln -s /opt/cmake-3.*your_version*/bin/* /usr/local/bin`
- Test your results with `cmake --version`

### 