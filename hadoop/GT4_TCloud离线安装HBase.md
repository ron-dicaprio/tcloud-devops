# 离线安装一套简陋的单副本HBase集群

## Hbase基础环境配置

### tbds下当前的HBase规划表

```shell
# Active Master Address
tbds-100-76-17-24(在用)
# Backup Master Address
tbds-100-76-17-28(备用)
# zookeeper Server
tbds-100-76-17-32:2181
tbds-100-76-17-21:2181
tbds-100-76-17-24:2181
tbds-100-76-17-20:2181
tbds-100-76-17-28:2181
# zookeeper client & regionservers
install zookeeper client in all nodes
regionservers include all nodes
```

### 操作系统及中间件

```shell
OS:CentOS Linux release 7.9.2009 (Core)
CPU:2Socket 2Core
Memory 4G
disk space:200G
java:openjdk version "1.8.0_431"
HBase:base on hadoop-3.2.1, version 2.2.7
# TBDS:5.2.0.1 * fuck tbds
```

### 本次集群规划表

```shell
# hbase version
https://devdoc.eu.org/packages/hbase-2.5.10-hadoop3-bin.tar.gz
# zookeeper version
https://devdoc.eu.org/packages/apache-zookeeper-3.8.4-bin.tar.gz
# zookeeper list
hdfs-86-105-132-169 zk3
hdfs-86-105-132-170 zk1
hdfs-86-105-132-171 zk2
# HBase master
hdfs-86-105-132-170 active master
hdfs-86-105-132-171 backup master
# regionserver
hdfs-86-105-132-169
hdfs-86-105-132-170
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

### 修改zookeeper的配置文件

#### zoo.cfg

```shell
# cp /opt/zookeeper3.8.4-bin/conf/zoo_sample.cfg /opt/zookeeper3.8.4-bin/conf/zoo.cfg
# cat zoo.cfg
# ...
# ZooKeeper 使用的毫秒为单位的时间单元，用于进行心跳，最小会话超时将是 tickTime 的两倍。
tickTime=2000
# 存储内存中数据库快照的位置。
dataDir=/data/zookeeper
# 数据库更新的事务日志所在目录。
dataLogDir=/data/zookeeper/log
# 监听客户端连接的端口。
clientPort=2181
# LF 初始通信时限，即集群中的 follower 服务器（F）与 leader 服务器（L）之间初始连接时能容忍的最多心跳数（tickTime的数量）。
initLimit=5
# LF 同步通信时限，即集群中的 follower 服务器（F）与 leader 服务器（L）之间请求和应答之间能容忍的最多心跳数（tickTime的数量）。
syncLimit=2
server.1=hdfs-86-105-132-170
server.2=hdfs-86-105-132-171
server.3=hdfs-86-105-132-169
# 指定自动清理事务日志和快照文件的频率，单位是小时。 
autopurge.purgeInterval=1
```

#### set myid

```shell
# set myid for each node
echo 1 > hdfs-86-105-132-170:/data/zookeeper/myid
echo 2 > hdfs-86-105-132-171:/data/zookeeper/myid
echo 3 > hdfs-86-105-132-169:/data/zookeeper/myid
```

#### set /bin/zkEnv.sh 

```shell
# cat /opt/zookeeper3.8.4-bin/bin/zkEnv.sh

# 修改 zkEnv.sh 文件中的ZK_SERVER_HEAP值，缺省为1000，单位是MB，修改为2048。
# default heap for zookeeper server
ZK_SERVER_HEAP="${ZK_SERVER_HEAP:-2048}"
```

### 配置HBase节点的java环境

```shell
# 每个datanode和namenode节点都要有Java环境
# https://devdoc.eu.org是我的S3存储服务器
# wget -c --no-check-certificate https://devdoc.eu.org/packages/jdk-8u431-linux-x64.tar.gz
tar -zxvf jdk-8u431-linux-x64.tar.gz -C /opt
echo 'export JAVA_HOME=/opt/jdk1.8.0_431' >> /etc/profile
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile
# echo 'export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib' >> /etc/profile
```

### 分发一下hosts配置

```shell
# vim /etc/hosts
86.105.132.170	hdfs-86.105.132.170
86.105.132.169	hdfs-86.105.132.169
86.105.132.168	hdfs-86.105.132.168
```

### 配置HBase节点的文件

#### hbase-env.sh

```shell
# cat /opt/hbase-2.5.10-hadoop3/conf/hbase-env.sh
export HBASE_HOME="/opt/hbase-2.5.10-hadoop3"
export JAVA_HOME="/usr/java/jdk1.8.0_202-amd64"
export HBASE_LOG_DIR=${HBASE_HOME}/logs
# HBASE_MANAGES_ZK设置true，使用 HBase自带的Zookeeper进行管理,flase采用集群模式
export HBASE_MANAGES_ZK=false
export HBASE_CLASSPATH="/opt/hadoop-3.2.1/etc/hadoop"
export HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP="true"
export HBASE_PID_DIR="/data/hbase"
```

#### regionservers

```shell
# cat /opt/hbase-2.5.10-hadoop3/conf/regionservers
hdfs-86.105.132.170
hdfs-86.105.132.169
hdfs-86.105.132.168
```

#### hbase-site.xml

```xml
# cat /opt/hbase-2.5.10-hadoop3/conf/hbase-site.xml
<configuration>

<property>
  <name>hbase.cluster.distributed</name>
  <value>true</value>
</property>

<property>
  <name>hbase.rootdir</name>
  <value>hdfs://hdfsCluster/hbase</value>
</property>

<property>
  <name>hbase.tmp.dir</name>
  <value>/data/tbase/tmp</value>
</property>

<property>
  <name>hbase.zookeeper.quorum</name>
  <value>hdfs-86.105.132.170:2181,hdfs-86.105.132.171:2181,hdfs-86.105.132.169:2181</value>
</property>

<!-- Zookeeper元数据快照的存储目录（需要和Zookeeper的zoo.cfg 配置文件中的属性一致）-->
<property>
  <name>hbase.zookeeper.property.dataDir</name>
  <value>/data/zookeeper</value>
</property>

<property>
  <name>hbase.unsafe.stream.capability.enforce</name>
  <value>false</value>
</property>

<property>
  <name>hbase.unsafe.stream.capability.enforce</name>
  <value>true</value>
</property>

<property>
  <name>hbase.wal.provider</name>
  <value>filesystem</value>
</property>

<!-- 为使用 Phoenix，hbase.client.keyvalue.maxsize 不能设置为 0 -->
<property>
  <name>hbase.client.keyvalue.maxsize</name>
  <value>10485760</value>
</property>

<property>
  <name>hbase.master.distributed.log.splitting</name>
  <value>true</value>
</property>

<!-- 一次 RPC 请求读取的数据行数，该参数设置有助于优化读取效率 -->
<property>
  <name>hbase.client.scanner.caching</name>
  <value>5000</value>
</property>

<!-- 当分区中 StoreFile 大小超过该值时，该分区可能会被拆分（受是否开启了自动 split 影响），
  一般线上集群会关闭 split 以免影响性能，因此会将该值设置的比较大，如 100G -->
<property>
  <name>hbase.hregion.max.filesize</name>
  <value>107374182400</value>
</property>

<property>
  <name>hbase.hregion.memstore.flush.size</name>
  <value>268435456</value>
</property>

<property>
  <name>hbase.regionserver.handler.count</name>
  <value>200</value>
</property>

<property>
  <name>hbase.regionserver.global.memstore.lowerLimit</name>
  <value>0.38</value>
</property>

<property>
  <name>hbase.hregion.memstore.block.multiplier</name>
  <value>8</value>
</property>

<property>
  <name>hbase.server.thread.wakefrequency</name>
  <value>1000</value>
</property>

<property>
  <name>hbase.rpc.timeout</name>
  <value>400000</value>
</property>

<!-- 当 HStore 的 StoreFile 数量超过该配置时，MemStore 刷新到磁盘之前需要进行拆分（split）
  或压缩（compact），除非超过 hbase.hstore.blockingWaitTime 配置的时间。因此，当禁止 
  自动主压缩（major compact）的时候该配置项一定要注意配置一个较大的值 -->
<property>
  <name>hbase.hstore.blockingStoreFiles</name>
  <value>5000</value>
</property>

<property>
  <name>hbase.client.scanner.timeout.period</name>
  <value>1000000</value>
</property>

<property>
  <name>zookeeper.session.timeout</name>
  <value>180000</value>
</property>

<property>
  <name>hbase.regionserver.optionallogflushinterval</name>
  <value>5000</value>
</property>

<property>
  <name>hbase.client.write.buffer</name>
  <value>5242880</value>
</property>

<!-- 当 HStore 的 StoreFile 数量超过该配置的值时，可能会触发压缩，该值不能设置得过大，否则
  会影响性能，一般建议设置为 3~5 -->
<property>
  <name>hbase.hstore.compactionThreshold</name>
  <value>5</value>
</property>

<property>
  <name>hbase.hstore.compaction.max</name>
  <value>12</value>
</property>

<!-- 将该值设置为 1 以禁止线上表的自动拆分（split），可以在建表的时候预分区或者之后手动分区 -->
<property>
  <name>hbase.regionserver.regionSplitLimit</name>
  <value>1</value>
</property>

<property>
  <name>hbase.regionserver.thread.compaction.large</name>
  <value>5</value>
</property>

<property>
  <name>hbase.regionserver.thread.compaction.small</name>
  <value>8</value>
</property>

<property>
  <name>hbase.master.logcleaner.ttl</name>
  <value>3600000</value>
</property>

<!-- 配置主压缩的时间间隔，0 表示禁止自动主压缩，如果是线上响应时间敏感的应用，则建议禁止而
  等到非高峰期手动压缩，否则很可能导致 HBase 响应超时而引起性能抖动 -->
<property>
  <name>hbase.hregion.majorcompaction</name>
  <value>0</value>
</property>

<property>
  <name>dfs.client.hedged.read.threadpool.size</name>
  <value>20</value>  <!-- 20 threads -->
</property>

<property>
  <name>dfs.client.hedged.read.threshold.millis</name>
  <value>5000</value>
</property>

</configuration>
```

#### backup-masters

```shell
# cat /opt/hbase-2.5.10-hadoop3/conf/backup-masters
hdfs-86.105.132.171
```

### 启动hbase

```shell
# bash start-hbase.sh

```







