#!/bin/bash
echo -e "开始执行$0"
echo -e "\033[31m---本工具用于一键安装zabbix服务端---\033[0m"
echo -e "Start Verify ROOT User..."

# Verify User
if [ `id -u` -eq 0 ];then
    echo -e "Current User Is Root..."
else
    echo -e "Current User Is Not Root. Exit..."
    exit 1
fi

# verify rpms
for rpm in "docker-ce";
do rpm -q $rpm || yum install -y $rpm ;
# 安装失败退出程序
if [ $? -ne 0 ]; then
    echo -e "Install $rpm Error, Exit..."
    exit 1
fi
done

# 开机自启动,重启docker 解决本地防火墙规则的问题
systemctl enable docker.service
systemctl restart docker.service

arch=`uname -m`
if [ $arch = "x86_64" ]; then
    echo -e "Current System arch is $arch, Start Load..."
else
    echo -e "Current System arch is $arch, Exit ..."
    exit 1
fi
echo -e "\033[31m---START---zabbix服务端开始---START---\033[0m"
# verify directory
dir=/tmp/auto_install
if [ -e $dir ];then
    rm -rf $dir/*
else
    mkdir $dir
fi

# tar -tf $dir/packages.tar.gz
# uname -m arch

sed -n -e '1,/^exit 0$/!p' $0 > ${dir}/packages.tgz 2>/dev/null

tar -zxvf ${dir}/packages.tgz -C ${dir}/
docker load -i ${dir}/docker_imgs/zabbix-mysql_5.7.tar
docker load -i ${dir}/docker_imgs/zabbix-server-mysql_5.4.9.tar
docker load -i ${dir}/docker_imgs/zabbix-web-nginx-mysql_5.4.9.tar
docker load -i ${dir}/docker_imgs/grafana_zabbix.tar

# Create docker network 
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

# zabbix web服务器用18080端口接入grafana
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
      -p 18080:8080 \
      -d zabbix-web-nginx-mysql:5.4.9

# grafana面板用80端口
docker run --name zabbix-grafana -it \
      --network zabbix_net \
      -e TZ="Asia/Shanghai" \
      --restart=always \
      -p 80:3000 \
      -d grafana:zabbix

echo -e "\033[31m---END---zabbix服务端安装完毕---END---\033[0m"
docker ps |grep zabbix

echo -e "\033[31mSTART---开始安装ansible---START\033[0m"
yum install -y $dir/ansible/*.rpm
echo -e "\033[31m---END---ansible安装完毕---END---\033[0m"

echo -e "\033[31m---zabbinx及ansible安装完毕,开始清理安装包---\033[0m"
rm -rf $dir/packages.tgz
rm -rf $dir/docker_imgs
rm -rf $dir/ansible
echo -e "\033[31m---安装包清理完毕---\033[0m"

# 防火墙开启则添加相应端口
systemctl is-active --quiet firewalld.service
if [ $? -eq 0 ]; then
    echo -e "firewalld.service is running"
    firewall-cmd --zone=public --add-port=10051/tcp --permanent
    firewall-cmd --zone=public --add-port=18080/tcp --permanent
    firewall-cmd --zone=public --add-port=80/tcp --permanent
    firewall-cmd --reload
fi

# shell 结束标记符
exit 0
