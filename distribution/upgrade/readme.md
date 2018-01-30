### 升级

1. 下载rancher-compose工具，[下载地址](https://releases.rancher.com/compose/v0.12.5/rancher-compose-windows-386-v0.12.5.zip)

2. 将rancher-compose-*.tar.gz放在docker宿主机上，解压，将其中的rancher-compose文件放置/usr/bin/目录下，并赋予执行权限

3. 修改doc文件夹下docker-compose文件中image地址，映射端口

4. 修改doc文件夹下rancher.conf文件，其中

   ```shell
   RANCHER_URL：可创建目标应用的环境端点
   RANCHER_ACCESS_KEY：可创建目标应用的环境端点的Access Key(用户名)
   RANCHER_SECRET_KEY：可创建目标应用的环境端点的Secret Key(密码)
   COMPOSE_PROJECT_NAME：创建后显示名称
   IMAGE_ADDRESS：需要的镜像（不含tag）,都是用latest
   ```

5. 赋予doc文件夹下upgrade.sh执行权限

6. 执行upgrade.sh脚本即可完成升级

