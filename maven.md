### install 命令
- 安装第三方tar包在maven本地仓库
  `mvn install:install-file -Dfile=dest.jar -DgroupId=com.ainnovation.opencv -DartifactId=opencv -Dversion=3.4.4 -Dpackaging=jar`

### archetype
> https://www.oracle.com/technetwork/cn/community/java/apache-maven-getting-started-2-405568-zhs.html
- `mvn archetype:generate -DgroupId=com.mycompany.helloworld -DartifactId=helloworld -Dpackage=com.mycompany.helloworld -Dversion=1.0-SNAPSHOT`
  

