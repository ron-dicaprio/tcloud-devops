# 离线安装一套简陋的单副本HDFS集群

## HDFS基础环境配置

### tbds下当前的HDFS规划表

```shell
# NameNode Address
tbds-100-76-17-29(在用),tbds-100-76-17-33(备用)
# NameNode Storage
/data/hadoop/hdfs/namenode
# DataNode Storage
/data/hadoop/hdfs/data
# zookeeper server (namenode HA)
tbds-100-76-17-32:2181,tbds-100-76-17-21:2181,tbds-100-76-17-24:2181,tbds-100-76-17-20:2181,tbds-100-76-17-28:2181
# zookeeper client
install zookeeper client in all datanodes
```

### 操作系统及中间件

```shell
OS:CentOS Linux release 7.9.2009 (Core)
CPU:2Socket 2Core
Memory 4G
disk space:200G
java:openjdk version "1.8.0_431"
HDFS:base on hadoop-3.2.1, HDFS version 2.5.0
# TBDS:5.2.0.1 * fuck tbds
```

### 本次集群规划表

```shell
# base url
https://cloud.tencent.com/developer/article/2394774?from_column=20421&from=20421
# NameNode Address
hdfs-86-105-132-170
# NameNode Storage
/data/hadoop/hdfs/namenode
# Datanode Storage
/data/hadoop/hdfs/datanode
# datanode Address
hdfs-86-105-132-169
hdfs-86-105-132-170(namenode+datanode)
hdfs-86-105-132-171
```

### 所有节点间主机配置免登陆

```shell
# nologin.sh同目录下创建ip_passwd_list文件
# cat ip_passwd_list
86.105.132.170 sysadmin
86.105.132.171 sysadmin
86.105.132.169 sysadmin
```

```shell
# cat nologin.sh
# 这个脚本按照自己喜好来改就行
#!/bin/bash
curdir=$(pwd)
cd $curdir

echo 'install sshpass and expect...'
if command -v yum > /dev/null;then
        yum install -y sshpass > /dev/null 2>&1
        yum install -y expect > /dev/null 2>&1
    else
        echo 'package manager yum not fund.'
fi

tar -zxvf ./packages.tar.gz

cur_arch=$(uname -m)
if [ $cur_arch == "x86_64" ];then
    rpm -qa | grep sshpass || test -e ./packages/sshpass-1.06-1.el7.x86_64.rpm && rpm -ivh ./packages/sshpass-1.06-1.el7.x86_64.rpm
    rpm -qa | grep expect  || test -e ./packages/expect-5.45-14.el7_1.x86_64.rpm && rpm -ivh ./packages/expect-5.45-14.el7_1.x86_64.rpm
else
    echo "Unsupport architecture $cur_arch" 
    exit 1
fi

rm -rf /root/.ssh/id_rsa /root/.ssh/id_rsa.pub /root/.ssh/known_hosts

expect -c "
spawn ssh-keygen

expect {
\"Enter file in which to save the key (/root/.ssh/id_rsa):\" {send \"\r\"; exp_continue}
\"Enter passphrase (empty for no passphrase):\" {send \"\r\"; exp_continue}
\"Enter same passphrase again:\" {send \"\r\"; exp_continue}
}"  #免交互执行ssh-keygen

ipcount=$(cat ip_passwd_list|wc -l)

for ((i=1;i<=$ipcount;i++));do
ip_eval=$(cat ip_passwd_list |awk '{print $1}'|head -n $i|tail -n 1)
passwd_eval=$(cat ip_passwd_list |awk '{print $2}'|head -n $i|tail -n 1)

expect -c "
spawn ssh $ip_eval -o StrictHostKeyChecking=no 

expect {
\"(yes/no)\" {send \"yes\r\"; exp_continue}
\"password:\" {send \"$passwd_eval\r\"; exit}
}"

echo $passwd_eval > /tmp/.nokey_pass
cp_pub_key=$(sshpass -f /tmp/.nokey_pass ssh $ip_eval 'mkdir -p .ssh && cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub)

done
rm -rf /tmp/.nokey_pass

# shell end sign
exit 0
```

### 配置hdfs节点的java环境

```shell
# 每个datanode和namenode节点都要有Java环境
# https://devdoc.eu.org是我的S3存储服务器
# wget -c --no-check-certificate https://devdoc.eu.org/packages/jdk-8u431-linux-x64.tar.gz
tar -zxvf jdk-8u431-linux-x64.tar.gz -C /opt
echo 'export JAVA_HOME=/opt/jdk1.8.0_431' >> /etc/profile
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile
# 使配置生效
source /etc/profile
# echo 'export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib' >> /etc/profile
```

### 创建hdfs用户账号(这一步不做，用root，因为我水平不够)

```shell
# 创建用户并给与登陆的权限
useradd -m hdfs -s /bin/bash
# 设置hdfs的密码
echo "hdfs:hdfs" | chpasswd
或者passwd hdfs来改
# 给与用户hdfs sudo的权限
usermod -aG wheel hdfs
```

### 分发一下hosts配置

```shell
# vim /etc/hosts
86.105.132.170	hdfs-86.105.132.170
86.105.132.169	hdfs-86.105.132.169
86.105.132.168	hdfs-86.105.132.168
```

## 修改hdfs的文件配置

> 以下是配置文件

### hadoop-env.sh

```shell
# cat /opt/hadoop-3.2.1/etc/hadoop/hadoop-env.sh
export JAVA_HOME="/opt/jdk1.8.0_431"
export HADOOP_HOME="/opt/hadoop-3.2.1"
export HADOOP_PID_DIR="/opt/hadoop-3.2.1"
export HDFS_NAMENODE_USER="root"
export HDFS_DATANODE_USER="root"
# export HDFS_DATANODE_SECURE_USER="root"
export HDFS_SECONDARYNAMENODE_USER="root"
export YARN_RESOURCEMANAGER_USER="root"
export YARN_NODEMANAGER_USER="root"
```

### core-site.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->
<configuration>
    <property>
      <name>fs.defaultFS</name>
      <value>hdfs://hdfs-86-105-132-170:8020</value>
      <final>true</final>
    </property>
    <property>
        <name>io.file.buffer.szie</name>
        <value>131072</value>
    </property>
    <property>
        <name>ha.zookeeper.quorum</name>
        <value>hdfs-86-105-132-170:2181,hdfs-86-105-132-171:2181,hdfs-86-105-132-169:2181</value>
    </property>
    <!-- 设置HDFS web UI用户身份 -->
    <property>
        <name>hadoop.http.staticuser.user</name>
        <value>root</value>
    </property>
    <!-- 配置该root允许通过代理访问的主机节点 -->
    <property>
        <name>hadoop.proxyuser.root.hosts</name>
        <value>*</value>
    </property>
    <!-- 对于每个<root>用户，hosts必须进行配置，而groups和users至少需要配置一个。-->
    <!-- 配置该root允许代理的用户所属组 -->
    <property>
        <name>hadoop.proxyuser.root.groups</name>
        <value>*</value>
    </property>
    <!-- 配置该root允许代理的用户 -->
    <property>
        <name>hadoop.proxyuser.root.users</name>
        <value>*</value>
    </property>
    <!-- 文件系统垃圾桶保存时间 -->
    <property>
        <name>fs.trash.interval</name>
        <value>1440</value>
    </property>
    <!-- 文件系统垃圾桶保存时间 -->
    <property>
      <name>hadoop.tmp.dir</name>
      <value>/data/hadoop/hdfs/tmp</value>
    </property>
</configuration>
```

### hdfs-site.xml

```xml
# cat /opt/hadoop-3.2.1/etc/hadoop/hdfs-site.xml 
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <!-- 为namenode集群定义一个services name，默认值：null -->
    <property>
        <name>dfs.nameservices</name>
        <value>hdfsCluster</value>
    </property>

    <!-- 配合 HBase 或其他 dfs 客户端使用，表示开启短路径读，可以用来优化客户端性能 -->
    <property>
        <name>dfs.client.read.shortcircuit</name>
        <value>true</value>
    </property>
    
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <!-- 说明：是否开启权限检查 -->
    <property>
        <name>dfs.permissions.enabled</name>
        <value>false</value>
    </property>
    
    <property>
        <name>dfs.namenode.rpc-address</name>
        <value>hdfs-86-105-132-170:8020</value>
    </property>

    <property>
        <name>dfs.datanode.address</name>
        <value>0.0.0.0:50010</value>
    </property>

    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/data/hadoop/hdfs/namenode</value>
        <final>true</final>
    </property>

    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/data/hadoop/hdfs/data</value>
        <final>true</final>
    </property>

    <property>
        <name>dfs.datanode.http.address</name>
        <value>0.0.0.0:50075</value>
    </property>

    <property>
        <name>dfs.permissions</name>
        <value>false</value>
    </property>

</configuration>
```

### mapred-site.xml

```xml
# cat /opt/hadoop-3.2.1/etc/hadoop/mapred-site.xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
    <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
    </property>
</configuration>
```

### yarn-site.xml

```xml
# cat /opt/hadoop-3.2.1/etc/hadoop/yarn-site.xml
<?xml version="1.0"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->
<configuration>

<!-- Site specific YARN configuration properties -->
    <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>hdfs-86-105-132-170</value>
    </property>

    <property>
      <name>yarn.nodemanager.address</name>
      <value>0.0.0.0:45454</value>
    </property>

    <property>
      <name>yarn.resourcemanager.scheduler.address</name>
      <value>hdfs-86-105-132-170:8030</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.bind-host</name>
      <value>0.0.0.0</value>
    </property>
    
    <property>
      <name>mapreduce.map.memory.mb</name>
      <value>2048</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
    </property>
</configuration>
```

### log4j.properties

```properties
# cat /opt/hadoop-3.2.1/etc/hadoop/log4j.properties
hadoop.root.logger=INFO,console
hadoop.log.dir=.
hadoop.log.file=hadoop.log
log4j.rootLogger=${hadoop.root.logger}, EventCounter
log4j.threshhold=ALL
log4j.appender.DRFA=org.apache.log4j.DailyRollingFileAppender
log4j.appender.DRFA.File=${hadoop.log.dir}/${hadoop.log.file}

log4j.appender.DRFA.DatePattern=.yyyy-MM-dd

log4j.appender.DRFA.layout=org.apache.log4j.PatternLayout

log4j.appender.DRFA.layout.ConversionPattern=%d{ISO8601} %p %c: %m%n

log4j.appender.console=org.apache.log4j.ConsoleAppender
log4j.appender.console.target=System.err
log4j.appender.console.layout=org.apache.log4j.PatternLayout
log4j.appender.console.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{2}: %m%n

hadoop.tasklog.taskid=null
hadoop.tasklog.iscleanup=false
hadoop.tasklog.noKeepSplits=4
hadoop.tasklog.totalLogFileSize=100
hadoop.tasklog.purgeLogSplits=true
hadoop.tasklog.logsRetainHours=12

log4j.appender.TLA=org.apache.hadoop.mapred.TaskLogAppender
log4j.appender.TLA.taskId=${hadoop.tasklog.taskid}
log4j.appender.TLA.isCleanup=${hadoop.tasklog.iscleanup}
log4j.appender.TLA.totalLogFileSize=${hadoop.tasklog.totalLogFileSize}

log4j.appender.TLA.layout=org.apache.log4j.PatternLayout
log4j.appender.TLA.layout.ConversionPattern=%d{ISO8601} %p %c: %m%n

hadoop.security.logger=INFO,console
hadoop.security.log.maxfilesize=256MB
hadoop.security.log.maxbackupindex=20
log4j.category.SecurityLogger=${hadoop.security.logger}
hadoop.security.log.file=SecurityAuth.audit
log4j.additivity.SecurityLogger=false
log4j.appender.DRFAS=org.apache.log4j.DailyRollingFileAppender
log4j.appender.DRFAS.File=${hadoop.log.dir}/${hadoop.security.log.file}
log4j.appender.DRFAS.layout=org.apache.log4j.PatternLayout
log4j.appender.DRFAS.layout.ConversionPattern=%d{ISO8601} %p %c: %m%n
log4j.appender.DRFAS.DatePattern=.yyyy-MM-dd

log4j.appender.RFAS=org.apache.log4j.RollingFileAppender
log4j.appender.RFAS.File=${hadoop.log.dir}/${hadoop.security.log.file}
log4j.appender.RFAS.layout=org.apache.log4j.PatternLayout
log4j.appender.RFAS.layout.ConversionPattern=%d{ISO8601} %p %c: %m%n
log4j.appender.RFAS.MaxFileSize=${hadoop.security.log.maxfilesize}
log4j.appender.RFAS.MaxBackupIndex=${hadoop.security.log.maxbackupindex}

hdfs.audit.logger=INFO,console
log4j.logger.org.apache.hadoop.hdfs.server.namenode.FSNamesystem.audit=${hdfs.audit.logger}
log4j.additivity.org.apache.hadoop.hdfs.server.namenode.FSNamesystem.audit=false
log4j.appender.DRFAAUDIT=org.apache.log4j.DailyRollingFileAppender
log4j.appender.DRFAAUDIT.File=${hadoop.log.dir}/hdfs-audit.log
log4j.appender.DRFAAUDIT.layout=org.apache.log4j.PatternLayout
log4j.appender.DRFAAUDIT.layout.ConversionPattern=%d{ISO8601} %p %c{2}: %m%n
log4j.appender.DRFAAUDIT.DatePattern=.yyyy-MM-dd

namenode.metrics.logger=INFO,NullAppender
log4j.logger.NameNodeMetricsLog=${namenode.metrics.logger}
log4j.additivity.NameNodeMetricsLog=false
log4j.appender.NNMETRICSRFA=org.apache.log4j.RollingFileAppender
log4j.appender.NNMETRICSRFA.File=${hadoop.log.dir}/namenode-metrics.log
log4j.appender.NNMETRICSRFA.layout=org.apache.log4j.PatternLayout
log4j.appender.NNMETRICSRFA.layout.ConversionPattern=%d{ISO8601} %m%n
log4j.appender.NNMETRICSRFA.MaxBackupIndex=1
log4j.appender.NNMETRICSRFA.MaxFileSize=64MB

mapred.audit.logger=INFO,console
log4j.logger.org.apache.hadoop.mapred.AuditLogger=${mapred.audit.logger}
log4j.additivity.org.apache.hadoop.mapred.AuditLogger=false
log4j.appender.MRAUDIT=org.apache.log4j.DailyRollingFileAppender
log4j.appender.MRAUDIT.File=${hadoop.log.dir}/mapred-audit.log
log4j.appender.MRAUDIT.layout=org.apache.log4j.PatternLayout
log4j.appender.MRAUDIT.layout.ConversionPattern=%d{ISO8601} %p %c{2}: %m%n
log4j.appender.MRAUDIT.DatePattern=.yyyy-MM-dd


log4j.appender.RFA=org.apache.log4j.RollingFileAppender
log4j.appender.RFA.File=${hadoop.log.dir}/${hadoop.log.file}

log4j.appender.RFA.MaxFileSize=256MB
log4j.appender.RFA.MaxBackupIndex=10

log4j.appender.RFA.layout=org.apache.log4j.PatternLayout
log4j.appender.RFA.layout.ConversionPattern=%d{ISO8601} %-5p %c{2} - %m%n
log4j.appender.RFA.layout.ConversionPattern=%d{ISO8601} %-5p %c{2} (%F:%M(%L)) - %m%n

hadoop.metrics.log.level=INFO
log4j.logger.org.apache.hadoop.metrics2=${hadoop.metrics.log.level}

log4j.logger.org.jets3t.service.impl.rest.httpclient.RestS3Service=ERROR

log4j.appender.NullAppender=org.apache.log4j.varia.NullAppender

log4j.appender.EventCounter=org.apache.hadoop.log.metrics.EventCounter

log4j.logger.org.apache.hadoop.conf.Configuration.deprecation=WARN

yarn.log.dir=.
hadoop.mapreduce.jobsummary.logger=${hadoop.root.logger}
hadoop.mapreduce.jobsummary.log.file=hadoop-mapreduce.jobsummary.log
log4j.appender.JSA=org.apache.log4j.DailyRollingFileAppender
yarn.server.resourcemanager.appsummary.log.file=hadoop-mapreduce.jobsummary.log
yarn.server.resourcemanager.appsummary.logger=${hadoop.root.logger}

log4j.appender.RMSUMMARY=org.apache.log4j.RollingFileAppender
log4j.appender.RMSUMMARY.File=${yarn.log.dir}/${yarn.server.resourcemanager.appsummary.log.file}
log4j.appender.RMSUMMARY.MaxFileSize=256MB
log4j.appender.RMSUMMARY.MaxBackupIndex=20
log4j.appender.RMSUMMARY.layout=org.apache.log4j.PatternLayout
log4j.appender.RMSUMMARY.layout.ConversionPattern=%d{ISO8601} %p %c{2}: %m%n
log4j.appender.JSA.layout=org.apache.log4j.PatternLayout
log4j.appender.JSA.layout.ConversionPattern=%d{yy/MM/dd HH:mm:ss} %p %c{2}: %m%n
log4j.appender.JSA.DatePattern=.yyyy-MM-dd
log4j.appender.JSA.layout=org.apache.log4j.PatternLayout
log4j.logger.org.apache.hadoop.yarn.server.resourcemanager.RMAppManager$ApplicationSummary=${yarn.server.resourcemanager.appsummary.logger}
log4j.additivity.org.apache.hadoop.yarn.server.resourcemanager.RMAppManager$ApplicationSummary=false

rm.audit.logger=${hadoop.root.logger}
log4j.logger.org.apache.hadoop.yarn.server.resourcemanager.RMAuditLogger=${rm.audit.logger}
log4j.additivity.org.apache.hadoop.yarn.server.resourcemanager.RMAuditLogger=false
log4j.appender.RMAUDIT=org.apache.log4j.DailyRollingFileAppender
log4j.appender.RMAUDIT.File=${yarn.log.dir}/rm-audit.log
log4j.appender.RMAUDIT.layout=org.apache.log4j.PatternLayout
log4j.appender.RMAUDIT.layout.ConversionPattern=%d{ISO8601} %p %c{2}: %m%n
log4j.appender.RMAUDIT.DatePattern=.yyyy-MM-dd

nm.audit.logger=${hadoop.root.logger}
log4j.logger.org.apache.hadoop.yarn.server.nodemanager.NMAuditLogger=${nm.audit.logger}
log4j.additivity.org.apache.hadoop.yarn.server.nodemanager.NMAuditLogger=false
log4j.appender.NMAUDIT=org.apache.log4j.DailyRollingFileAppender
log4j.appender.NMAUDIT.File=${yarn.log.dir}/nm-audit.log
log4j.appender.NMAUDIT.layout=org.apache.log4j.PatternLayout
log4j.appender.NMAUDIT.layout.ConversionPattern=%d{ISO8601} %p %c{2}: %m%n
log4j.appender.NMAUDIT.DatePattern=.yyyy-MM-dd
```

## 集群初始化

### 运行datanode

```shell
1、在namemode上执行初始化
# hadoop namenode -format
2、datanode节点不需要执行hadoop namenode -format
3、在namemode上运行hdfs
# bash start-dfs.sh
4、在datanode上执行数据节点初始化和纳管
# bash hadoop-daemon start datanode
```

### hdfs常用命令

#### 1、在namenode上查看所有的datanode节点

```shell
# hdfs dfsadmin -report
Configured Capacity: 54716792832 (50.96 GB)
Present Capacity: 39475245056 (36.76 GB)
DFS Remaining: 39475204096 (36.76 GB)
DFS Used: 40960 (40 KB)
DFS Used%: 0.00%
Replicated Blocks:
        Under replicated blocks: 0
        Blocks with corrupt replicas: 0
        Missing blocks: 0
        Missing blocks (with replication factor 1): 0
        Low redundancy blocks with highest priority to recover: 0
        Pending deletion blocks: 0
Erasure Coded Block Groups: 
        Low redundancy block groups: 0
        Block groups with corrupt internal blocks: 0
        Missing block groups: 0
        Low redundancy blocks with highest priority to recover: 0
        Pending deletion blocks: 0

-------------------------------------------------
Live datanodes (3):

Name: 86.105.132.169:50010 (hdfs-86-105-132-169)
Hostname: hdfs-86-105-132-169
Decommission Status : Normal
Configured Capacity: 18238930944 (16.99 GB)
DFS Used: 8192 (8 KB)
Non DFS Used: 2971070464 (2.77 GB)
DFS Remaining: 15267852288 (14.22 GB)
DFS Used%: 0.00%
DFS Remaining%: 83.71%
Configured Cache Capacity: 0 (0 B)
Cache Used: 0 (0 B)
Cache Remaining: 0 (0 B)
Cache Used%: 100.00%
Cache Remaining%: 0.00%
Xceivers: 1
Last contact: Mon Jan 13 11:18:21 CST 2025
Last Block Report: Mon Jan 13 10:18:09 CST 2025
Num of Blocks: 0

Name: 86.105.132.170:50010 (hdfs-86-105-132-170)
Hostname: hdfs-86-105-132-170
Decommission Status : Normal
Configured Capacity: 18238930944 (16.99 GB)
DFS Used: 24576 (24 KB)
Non DFS Used: 8790573056 (8.19 GB)
DFS Remaining: 9448333312 (8.80 GB)
DFS Used%: 0.00%
DFS Remaining%: 51.80%
Configured Cache Capacity: 0 (0 B)
Cache Used: 0 (0 B)
Cache Remaining: 0 (0 B)
Cache Used%: 100.00%
Cache Remaining%: 0.00%
Xceivers: 1
Last contact: Mon Jan 13 11:18:22 CST 2025
Last Block Report: Mon Jan 13 09:42:08 CST 2025
Num of Blocks: 1

Name: 86.105.132.171:50010 (hdfs-86-105-132-171)
Hostname: hdfs-86-105-132-171
Decommission Status : Normal
Configured Capacity: 18238930944 (16.99 GB)
DFS Used: 8192 (8 KB)
Non DFS Used: 3479904256 (3.24 GB)
DFS Remaining: 14759018496 (13.75 GB)
DFS Used%: 0.00%
DFS Remaining%: 80.92%
Configured Cache Capacity: 0 (0 B)
Cache Used: 0 (0 B)
Cache Remaining: 0 (0 B)
Cache Used%: 100.00%
Cache Remaining%: 0.00%
Xceivers: 1
Last contact: Mon Jan 13 11:18:23 CST 2025
Last Block Report: Mon Jan 13 10:54:14 CST 2025
Num of Blocks: 0
```

#### 2、hdfs文件及目录操作
```shell
1、上传hdfs.tgz文件到hdfs的根目录上
# hadoop fs -put hdfs.tgz hdfs:///
2、查看文件根目录磁盘使用情况
# hadoop fs -du -s -h /
3、todo
```







