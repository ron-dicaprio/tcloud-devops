#!/bin/bash

## filename : install_zabbix_agent.sh
## version  : v1.0
## date     : 20230811
## author   : f-CSS

echo -e "开始执行$0"
echo -e "\033[31m---本工具用于一键安装zabbix客户端---\033[0m"
echo -e "Start Verify ROOT User..."

# Verify User
if [ `id -u` -eq 0 ];then
    echo -e "Current User Is Root..."
else
    echo -e "Current User Is Not Root. Exit..."
    exit 1
fi

# verify directory
dir=/tmp/auto_install
if [ -e $dir ];then
    rm -rf $dir/*
else
    mkdir $dir
fi

# rewrite tar
sed -n -e '1,/^exit 0$/!p' $0 > ${dir}/packages.tgz 2>/dev/null

# unzip 
tar -zxvf ${dir}/packages.tgz -C ${dir}/

# verify rpms
for rpm in "net-tools";
do rpm -q $rpm || yum install -y $rpm ;
# 安装失败之后从本地安装
if [ $? -ne 0 ]; then
    yum install -y ${dir}/net_tools/net-tools-2.0-0.25.20131004git.el7.x86_64.rpm
    echo -e "Installed $rpm from local files..."
fi
done

# install zabbix agent
rpm -ivh ${dir}/zabbix_agent/zabbix-agent2-5.0.36-1.el7.x86_64.rpm

local_ip=`ifconfig ens33|grep netmask|awk '{print $2}'`
echo -e "本地IP地址为：$local_ip"


# 获取服务器地址
read -p "请输入zabbix服务器IP地址:" server_ip

# 修改Server的值
sed -i "s/Server=127.0.0.1/Server=$server_ip/g" /etc/zabbix/zabbix_agent2.conf

# 修改ServerActive的值
sed -i "s/ServerActive=127.0.0.1/ServerActive=$server_ip/g" /etc/zabbix/zabbix_agent2.conf

#  Hostname=Zabbix server
sed -i "s/Hostname=Zabbix server/Hostname=$local_ip/g" /etc/zabbix/zabbix_agent2.conf

#  Timeout=30
sed -i "s/# Timeout=3/Timeout=30/g" /etc/zabbix/zabbix_agent2.conf

# 防火墙开启则添加tcp10050端口
systemctl is-active --quiet firewalld.service
if [ $? -eq 0 ]; then
    echo -e "firewalld.service is running"
    firewall-cmd --zone=public --add-port=10050/tcp --permanent
    firewall-cmd --reload
fi

# enable zabbix-agent2
systemctl restart zabbix-agent2
systemctl enable zabbix-agent2

rm -rf $dir/packages.tgz
rm -rf $dir/net_tools
rm -rf $dir/zabbix_agent
echo -e "\033[31m---安装包清理完毕---\033[0m"

# exit sign
exit 0
