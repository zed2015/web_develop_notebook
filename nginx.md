# nginx 配置说明

##  nginx location配置优先级别

模式    含义
location = /uri = 表示精确匹配，只有完全匹配上才能生效
location ^~ /uri    ^~ 开头对URL路径进行前缀匹配，并且在正则之前。
location ~ pattern  开头表示区分大小写的正则匹配
location ~\* pattern 开头表示不区分大小写的正则匹配
location /uri   不带任何修饰符，也表示前缀匹配，但是在正则匹配之后
location /  通用匹配，任何未匹配到其它location的请求都会匹配到，相当于switch中的default

## nginx 设置代理转发的特定头部
proxy_set_header X-Real-IP $remote_ip

## try_file rewrite的理解
- try_file $uri $uri/ @rewrites
> 尝试读取文件或文件夹， 如果找不到那么会跳到rewiretes的location
- rewrites re replace [lask, break]
> 将正则匹配的替换为replace的东西，后面是flag标记， 
- rewrite_log on;
> 当报错时，可以开启日志功能
- rewrite 会优先 location进行匹配

## 访问一个网站时，浏览器会主动访问$host/favicon.ico
> 导致nginx 访问日志出现404
```
location = /favicon.ico {
  log_not_found off;
  access_log off;
}

```
## error_page指定的解释
> 当发生作物的时候能够显示一个预定义的uri
- `error_page 502 503  /50x.html`
> 相当如产生了一个内部internal redirect
- `error_page 403 http://example.com/forbiddent.hmtl`
> 默认返回302重定向
- `error_page 502 503 =200  /50x.html`
> 可以指定返回的转该码
- `error_page`不会gizp


## internal 指定
- contenxt is location
- requests redirected by the “X-Accel-Redirect” response header field from an upstream server
- requests changed by the rewrite directive.
- requests redirected by the error_page, index, random_index, and try_files directives





