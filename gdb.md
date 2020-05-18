#### python 调试分析经典文章
- `https://drmingdrmer.github.io/tech/programming/2017/05/06/python-mem.html#gdb-python-%E6%90%9E%E6%B8%85%E6%A5%9Apython%E7%A8%8B%E5%BA%8F%E5%9C%A8%E5%81%9A%E4%BB%80%E4%B9%88`
- `https://wiki.python.org/moin/DebuggingWithGdb`
- `https://www.podoliaka.org/2016/04/10/debugging-cpython-gdb/`

#### python gdb 调试
- install `sudo apt-get install gdb python2.7-dbg`
- `gdb python pid`
- `info auto-load, source ...`
- usr/share/gdb/auto-load/usr/bin

#### pyrasite
- echo 0 > /proc/sys/kernel/yama/ptrace_scope
- pip install pyrasite
- pyrasite-shell pid
- 
