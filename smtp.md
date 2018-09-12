## linux 安装sendmail
### 安装程序
- `sudo apt-get install sendmail`
- `sudo apt-get install sendmail-cf`
- `ps aux |grep sendmail`
- `sudo apt-get install mailutils`
### 修改配置文件
- `vim /etc/mail/sendmail.mc`
- `EMON_OPTIONS(Family=inet,  Name=MTA-v4, Port=smtp, Addr=127.0.0.1')dnl`
  > 127.0.0.1 --> 0.0.0.0
- 保存配置文件
```
cd /etc/mail
mv sendmail.cf sendmail.cf.bak
m4 sendmail.mc > sendmail.cf
```
- 修改host文件
  > `127.0.0.1 domain.com`
- `telnet 127.0.0.1 25`
- `sendmail -t <<EOF`

```
EHLO
auth login
mail from:
rcpt to:
data
.
```



