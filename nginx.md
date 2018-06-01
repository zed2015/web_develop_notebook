# nginx 配置说明

##  nginx location配置优先级别

模式    含义
location = /uri = 表示精确匹配，只有完全匹配上才能生效
location ^~ /uri    ^~ 开头对URL路径进行前缀匹配，并且在正则之前。
location ~ pattern  开头表示区分大小写的正则匹配
location ~* pattern 开头表示不区分大小写的正则匹配
location /uri   不带任何修饰符，也表示前缀匹配，但是在正则匹配之后
location /  通用匹配，任何未匹配到其它location的请求都会匹配到，相当于switch中的default

