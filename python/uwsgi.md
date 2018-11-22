### uwsgi 参考资料

#### http， socket, http-socket 协议
- 如果protocol配置参数理有http选项，就会时http协议，可以独立处理http请求
- protocol 默认时socket协议，即用的uwsgi协议，nginx需要通过uwsgi-pass参数来转送请求

#### 配置参数说明
- http  设置http的ip端口
- uwsgi-socket 
- http-socket

