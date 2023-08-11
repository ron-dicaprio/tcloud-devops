# How To Install Zabbix 5.0 LTS in Cnetos 7.9

## 
```sh
# 设计思路

zabbix-server-mysql,zabbix-web-nginx-mysql,mysql, grafana用docker部署。
agent 用RPM的方式部署和接入

为了方便离线安装，可制作成bin包的方式分发
zabbix server本机安装ansible实现批量下发bin包

后续考虑传参的方式接收zabbix server的地址，或者写死也行
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

# 查看端口转发情况
ss -lnt

```

# get key via zabbix server
zabbix_get -s 10.0.0.110 -p 10050 -k "system.hostname"


# zabbix监控的话，时间同步很重要 
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
hwclock -w

# 重启服务并设置开机自启动
systemctl restart zabbix-agent2
systemctl enable zabbix-agent2

# 设置hostname 非必要
hostnamectl set-hostname 10.0.0.111
hostname -F /etc/hostname
