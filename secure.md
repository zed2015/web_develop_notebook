## SSH 原理
> 参考链接 https://www.jianshu.com/p/33461b619d53

### 对称加密
- 加密、解密都是用的同一个密钥
- 多个client 会保存这个密钥，因此这个密钥一旦被丢，就很危险

### 非对称加密
- 加密、解密用的不同的密钥
- 加密过程
    - client 向 server 端请求时， server端会将 public_key给client
    - client用公钥pubulic_key给传输内容加密，将加密后的内容发送给server端
    - server 端用私钥secret_key对内容进行解密，然后进行验证
- 风险
> 中间人攻击
    - 不能保证我请求服务的正确性，黑客会冒充我们的server端，获取到我们内容
    - 如何对server端的公钥进行认证？https中的CA就可以认证
    - ssh的public_key, secret_key是自己生成的，如何验证?
    - 通过client对自己的公钥进行确认
- SSH 密钥登录
    - client端的public_key手动copy到server端， SSH 建立链接的过程中没有公钥的交换过程， 
    - client 端在认证的死后开始会发送一个keyID给server, 这个keyID唯一对应client的Public_key
    - server端通过keyID在authorized_keys进行查找对应的Public_key,并生成随机数R， 用Client的公钥对随机数R进行加密得到pubulic(R), 然后将加密信息发送给client
    - client 用私钥解密public(R)得到R, 随机数R及本次会话的SessionKey利用MD5生成摘要Digest1, 发送给Server端
    - server端也会对R和SessionKey利用同样的摘要算法生成Digest2, 最后比较Digest1与Digest2是否相同，完成认证过程
### passphrase 是保护私钥
> 当我们想要别人登录我们服务器时，但是不想将root密码给别人，可以将带有passphrase的 id_rsa给别人，别人用这个登录时，需要提供 passphrase即可




