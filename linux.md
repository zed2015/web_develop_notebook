## 更改用户名的uid与gid
```
usermod -u uid username
groupmod -g gid groupname

```
## SSH 操作 
- 生成ssh钥匙, 指定密码
`ssh-keygen -f ~/.ssh/id_rsa_spc -p'123456'`

- 上传公钥匙到远程机器的authorized_keys里
`ssh-copy-id -i /home/zc/.ssh/id_rsa.pub root@ip`

- 指定特定的私密钥匙进行认证
`ssh -i ~/.ssh/id_rsa_spec root@ip`

- 代理的使用
    - `ssh-agent bash`
    - `ssh-add ~/.ssh/id_rsa_spec`
    - `ssh-add -l[-L]`





