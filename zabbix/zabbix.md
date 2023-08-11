# How To Install Zabbix 5.0 LTS in Cnetos 7.x

## 
```sh
# 设计思路
zabbix-server-mysql,zabbix-web-nginx-mysql,mysql 5.7.43 用docker部署。

agent 用RPM的方式部署和接入
```
## download packages
```sh
docker pull mysql:5.7
docker pull zabbix/zabbix-server-mysql:centos-latest
docker pull zabbix/zabbix-web-nginx-mysql:latest

#
docker network create -d bridge zabbix_net


docker run --name zabbix-mysql -it \
      -e TZ="Asia/Shanghai" \
      -e TZ="Asia/Shanghai" \
      --network zabbix_net \
      --restart=always \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="Epointadmin#2023" \
      -e MYSQL_ROOT_PASSWORD="Epointadmin#2023" \
      -e TZ="Asia/Shanghai" \
      -p 3306:3306 \
      -d zabbix-mysql:5.7

docker run --name zabbix-server-mysql -it \
      -e TZ="Asia/Shanghai" \
      --network zabbix_net \
      --restart=always \
      -e DB_SERVER_HOST="zabbix-mysql" \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="Epointadmin#2023" \
      -e MYSQL_ROOT_PASSWORD="Epointadmin#2023" \
      --link zabbix-mysql:mysql \
      -p 10051:10051 \
      -d zabbix-server-mysql:5.4.9

docker run --name zabbix-web-nginx-mysql -it \
      -e TZ="Asia/Shanghai" \
      --network zabbix_net \
      --restart=always \
      -e DB_SERVER_HOST="zabbix-mysql" \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="Epointadmin#2023" \
      -e MYSQL_ROOT_PASSWORD="Epointadmin#2023" \
      --link zabbix-mysql:mysql \
      --link zabbix-server-mysql:zabbix-server \
      -p 80:8080 \
      -d zabbix-web-nginx-mysql:5.4.9

docker run --name zabbix-grafana -it \
      -e TZ="Asia/Shanghai" \
      --restart=always \
      -p 3000:3000 \
      -d grafana:zabbix


# 不建议用docker跑，一定要挂载配置文件
docker run --name zabbix-agent  -it \
      -e TZ="Asia/Shanghai" \
      -e ZBX_HOSTNAME="Zabbix server" \
      -e ZBX_SERVER_HOST=10.0.0.100 \
      -e ZBX_SERVER_PORT=10051 \
      --privileged \
      --restart unless-stopped \
      -p 10050:10050 \
      -d zabbix/zabbix-agent:latest


# 查看端口转发情况
ss -lnt

#select * from user;
#update user set authentication_string=password('Epointadmin#2023');
#flush privileges;


# 安装docker
mv /usr/lib/systemd/system/docker.service /data/
yum reinstall *.rpm
systemctl daemon-reload
systemctl restart docker.service

docker run --name mysql-server -t \
      -e MYSQL_DATABASE="zabbix" \
      -e MYSQL_USER="zabbix" \
      -e MYSQL_PASSWORD="zabbix_pwd" \
      -e MYSQL_ROOT_PASSWORD="root_pwd" \
      -d mysql:5.7

docker run --name zabbix-server -e DB_SERVER_HOST="10.0.0.100" -e MYSQL_USER="root" -e MYSQL_PASSWORD="Epointadmin#2023" -d  -p 10051:10051 zabbix-server-mysql:latest
docker run --name zabbix-web-nginx -e DB_SERVER_HOST="10.0.0.100" -e MYSQL_USER="root" -e MYSQL_PASSWORD="Epointadmin#2023" -e ZBX_SERVER_HOST="10.0.0.100" -e PHP_TZ="Asia/shanghai" -d zabbix-web-nginx-mysql:latest
```

# get key
zabbix_get -s 10.0.0.110 -p 10050 -k "system.hostname"

#
cd /etc/zabbix/

# 时间同步很重要 
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
hwclock -w

# 重启服务并设置开机自启动
systemctl restart zabbix-agent2
systemctl enable zabbix-agent2

# 设置hostname
hostnamectl set-hostname 10.0.0.111
hostname -F /etc/hostname