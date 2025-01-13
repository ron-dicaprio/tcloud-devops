# HDFS Configs

### ENV Config

```shell
# java -version
openjdk version "1.8.0_292"
OpenJDK Runtime Environment (Tencent Kona 8.0.6-internal) (build 1.8.0_292-b1)
OpenJDK 64-Bit Server VM (Tencent Kona 8.0.6-internal) (build 25.292-b1, mixed mode, sharing)
# cat /etc/redhat-release 
CentOS Linux release 7.4 (Final)
# host 
2Socket 64CPU 128Thread 64GRAM 7.3T_HardDrive
```

### HDFS config

#### hadoop-env.sh

```shell
# cat /usr/hdp/current/hadoop-hdfs-client/etc/hadoop/hadoop-env.sh
export JAVA_HOME=/usr/jdk64/jdk1.8.0_191
export HADOOP_HOME_WARN_SUPPRESS=1
export HADOOP_HOME=${HADOOP_HOME:-/usr/hdp/2.2.0.0-2041/hadoop}
export JSVC_HOME=/usr/lib/bigtop-utils
export HADOOP_HEAPSIZE="4096"
export HADOOP_NAMENODE_INIT_HEAPSIZE="-Xms81920m"
export HADOOP_OPTS="-Djava.net.preferIPv4Stack=true ${HADOOP_OPTS}"
USER="$(whoami)"
HADOOP_JOBTRACKER_OPTS="-server -XX:ParallelGCThreads=8 -XX:+UseConcMarkSweepGC -XX:ErrorFile=/var/log/hadoop/$USER/hs_err_pid%p.log -XX:NewSize=200m -XX:MaxNewSize=200m -Xloggc:/var/log/hadoop/$USER/gc.log-`date +'%Y%m%d%H%M'` -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -Xmx1024m -Dhadoop.security.logger=INFO,DRFAS -Dmapred.audit.logger=INFO,MRAUDIT -Dhadoop.mapreduce.jobsummary.logger=INFO,JSA ${HADOOP_JOBTRACKER_OPTS}"

HADOOP_TASKTRACKER_OPTS="-server -Xmx1024m -Dhadoop.security.logger=ERROR,console -Dmapred.audit.logger=ERROR,console ${HADOOP_TASKTRACKER_OPTS}"

export HADOOP_NAMENODE_OPTS="-server -XX:ParallelGCThreads=8 -XX:+UseConcMarkSweepGC -XX:ErrorFile=/var/log/hadoop/$USER/hs_err_pid%p.log -XX:NewSize=10240m -XX:MaxNewSize=10240m -Xloggc:/var/log/hadoop/$USER/gc.log-`date +'%Y%m%d%H%M'` -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -XX:CMSInitiatingOccupancyFraction=70 -XX:+UseCMSInitiatingOccupancyOnly -Xms81920m -Xmx81920m -Dhadoop.security.logger=INFO,DRFAS -Dhdfs.audit.logger=INFO,DRFAAUDIT -Dnamenode.metrics.logger=INFO,NNMETRICSRFA ${HADOOP_NAMENODE_OPTS} -Dorg.mortbay.jetty.Request.maxFormContentSize=-1"
export HADOOP_DATANODE_OPTS="-server -XX:CMSInitiatingOccupancyFraction=70 -XX:+UseCMSInitiatingOccupancyOnly -XX:ParallelGCThreads=4 -XX:+UseConcMarkSweepGC -XX:ErrorFile=/var/log/hadoop/$USER/hs_err_pid%p.log -XX:NewSize=200m -XX:MaxNewSize=200m -Xloggc:/var/log/hadoop/$USER/gc.log-`date +'%Y%m%d%H%M'` -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:+PrintGCDateStamps -Xms4096m -Xmx4096m -Dhadoop.security.logger=INFO,DRFAS -Dhdfs.audit.logger=INFO,DRFAAUDIT ${HADOOP_DATANODE_OPTS}"

IP_ADDR=$(ip route get 8.8.8.8 | grep dev | awk -F"src" '{print $2;}' | awk '{print $1;}')
export HADOOP_NAMENODE_OPTS="-Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false  -Djava.rmi.server.hostname=$IP_ADDR   -Dcom.sun.management.jmxremote.local.only=false   -Dcom.sun.management.jmxremote.port=8700  $HADOOP_NAMENODE_OPTS "
export HADOOP_DATANODE_OPTS="-Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false  -Djava.rmi.server.hostname=$IP_ADDR   -Dcom.sun.management.jmxremote.local.only=false   -Dcom.sun.management.jmxremote.port=8701 $HADOOP_DATANODE_OPTS"

export HADOOP_CLIENT_OPTS="-Xmx${HADOOP_HEAPSIZE}m $HADOOP_CLIENT_OPTS"

HADOOP_BALANCER_OPTS="-server -Xmx4096m ${HADOOP_BALANCER_OPTS}"

export HADOOP_SECONDARYNAMENODE_OPTS=$HADOOP_NAMENODE_OPTS
export HADOOP_SECURE_DN_USER=${HADOOP_SECURE_DN_USER:-""}
export HADOOP_SSH_OPTS="-o ConnectTimeout=5 -o SendEnv=HADOOP_CONF_DIR"
export HADOOP_LOG_DIR=/var/log/hadoop/$USER
export HADOOP_MAPRED_LOG_DIR=/var/log/hadoop-mapreduce/$USER
export HADOOP_SECURE_DN_LOG_DIR=/var/log/hadoop/$HADOOP_SECURE_DN_USER
export HADOOP_PID_DIR=/var/run/hadoop/$USER
export HADOOP_SECURE_DN_PID_DIR=/var/run/hadoop/$HADOOP_SECURE_DN_USER
export HADOOP_MAPRED_PID_DIR=/var/run/hadoop-mapreduce/$USER

YARN_RESOURCEMANAGER_OPTS="-Dyarn.server.resourcemanager.appsummary.logger=INFO,RMSUMMARY"

export HADOOP_IDENT_STRING=$USER

JAVA_JDBC_LIBS=""
if [ -d "/usr/share/java" ]; then
  for jarFile in `ls /usr/share/java | grep -E "(mysql|ojdbc|postgresql|sqljdbc)" 2>/dev/null`
  do
    JAVA_JDBC_LIBS=${JAVA_JDBC_LIBS}:$jarFile
  done
fi

MAPREDUCE_LIBS=/usr/hdp/current/hadoop-mapreduce-client/*

export HADOOP_CLASSPATH=${HADOOP_CLASSPATH}${JAVA_JDBC_LIBS}:${MAPREDUCE_LIBS}

if [ -d "/usr/hdp/current/tez-client" ]; then
  if [ -d "/etc/tez/conf/" ]; then
    export HADOOP_CLASSPATH=${HADOOP_CLASSPATH}:/usr/hdp/current/tez-client/*:/usr/hdp/current/tez-client/lib/*:/etc/tez/conf/
  fi
fi

export HADOOP_LIBEXEC_DIR=/usr/hdp/2.2.0.0-2041/hadoop/libexec
export JAVA_LIBRARY_PATH=${JAVA_LIBRARY_PATH}:/usr/hdp/2.2.0.0-2041/hadoop/lib/native/Linux-amd64-64
export HADOOP_OPTS="-Dhdp.version=$HDP_VERSION $HADOOP_OPTS"
```

#### core-site.xml

```xml
# cat /usr/hdp/current/hadoop-hdfs-client/etc/hadoop/core-site.xml 
  <configuration  xmlns:xi="http://www.w3.org/2001/XInclude">
    
    <property>
      <name>fs.azure.user.agent.prefix</name>
      <value>User-Agent: APN/1.0 Hortonworks/1.0 HDP/</value>
    </property>
    
    <property>
      <name>fs.defaultFS</name>
      <value>hdfs://hdfsCluster</value>
      <final>true</final>
    </property>
    
    <property>
      <name>fs.gs.application.name.suffix</name>
      <value> (GPN:Hortonworks; version 1.0) HDP/</value>
    </property>
    
    <property>
      <name>fs.gs.path.encoding</name>
      <value>uri-path</value>
    </property>
    
    <property>
      <name>fs.gs.working.dir</name>
      <value>/</value>
    </property>
    
    <property>
      <name>fs.s3a.user.agent.prefix</name>
      <value>User-Agent: APN/1.0 Hortonworks/1.0 HDP/</value>
    </property>
    
    <property>
      <name>fs.trash.interval</name>
      <value>360</value>
    </property>
    
    <property>
      <name>ha.failover-controller.active-standby-elector.zk.op.retries</name>
      <value>120</value>
    </property>
    
    <property>
      <name>ha.zookeeper.quorum</name>
      <value>tbds-100-76-17-32:2181,tbds-100-76-17-21:2181,tbds-100-76-17-24:2181,tbds-100-76-17-20:2181,tbds-100-76-17-28:2181</value>
    </property>
    
    <property>
      <name>ha.zookeeper.session-timeout.ms</name>
      <value>180000</value>
    </property>
    
    <property>
      <name>hadoop.http.authentication.simple.anonymous.allowed</name>
      <value>true</value>
    </property>
    
    <property>
      <name>hadoop.httpfs.port</name>
      <value>14000</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.*</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.ftponhdfs.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.ftponhdfs.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hbase.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hbase.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hcat.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hcat.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hdfs.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hdfs.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hippo.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hippo.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hive.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hive.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.httpfs.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.httpfs.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hue.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.hue.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.idex.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.idex.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.jstorm.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.jstorm.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.livy.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.livy.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.olap.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.olap.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.root.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.root.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.streamingsql.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.streamingsql.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.tbds.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.tbds.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.tbdsalarm.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.tbdsalarm.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.tbdsmetadata.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.tbdsmetadata.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.yarn.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.proxyuser.yarn.hosts</name>
      <value>*</value>
    </property>
    
    <property>
      <name>hadoop.security.auth_to_local</name>
      <value>DEFAULT</value>
    </property>
    
    <property>
      <name>hadoop.security.authentication</name>
      <value>simple</value>
    </property>
    
    <property>
      <name>hadoop.security.authorization</name>
      <value>false</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping</name>
      <value>org.apache.hadoop.security.LdapGroupsMapping</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.base</name>
      <value>dc=tbds,dc=com</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.bind.password</name>
      <value>admin</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.bind.user</name>
      <value>cn=admin,dc=tbds,dc=com</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.search.attr.group.name</name>
      <value>cn</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.search.attr.member</name>
      <value>member</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.search.filter.group</name>
      <value>(objectClass=groupOfNames)</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.search.filter.user</name>
      <value>(&amp;(objectClass=inetOrgPerson)(cn={0}))</value>
    </property>
    
    <property>
      <name>hadoop.security.group.mapping.ldap.url</name>
      <value>ldap://tbds-100-76-17-4:389</value>
    </property>
    
    <property>
      <name>hadoop.security.key.provider.path</name>
      <value></value>
    </property>
    
    <property>
      <name>hadoop.tmp.dir</name>
      <value>/tmp</value>
    </property>
    
    <property>
      <name>io.compression.codecs</name>
      <value>org.apache.hadoop.io.compress.GzipCodec,org.apache.hadoop.io.compress.DefaultCodec,org.apache.hadoop.io.compress.SnappyCodec</value>
    </property>
    
    <property>
      <name>io.file.buffer.size</name>
      <value>131072</value>
    </property>
    
    <property>
      <name>io.serializations</name>
      <value>org.apache.hadoop.io.serializer.WritableSerialization</value>
    </property>
    
    <property>
      <name>ipc.client.connect.max.retries</name>
      <value>50</value>
    </property>
    
    <property>
      <name>ipc.client.connection.maxidletime</name>
      <value>30000</value>
    </property>
    
    <property>
      <name>ipc.client.idlethreshold</name>
      <value>8000</value>
    </property>
    
    <property>
      <name>ipc.server.tcpnodelay</name>
      <value>true</value>
    </property>
    
    <property>
      <name>mapreduce.jobtracker.webinterface.trusted</name>
      <value>false</value>
    </property>
    
    <property>
      <name>tbds.portal.rpc.ip</name>
      <value></value>
    </property>
    
    <property>
      <name>tbds.portal.rpc.port</name>
      <value>default</value>
    </property>
```

#### hdfs-site.xml

```xml
# cat /usr/hdp/current/hadoop-hdfs-client/etc/hadoop/hdfs-site.xml
<configuration  xmlns:xi="http://www.w3.org/2001/XInclude">
    
    <property>
      <name>dfs.block.access.token.enable</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.blockreport.initialDelay</name>
      <value>120</value>
    </property>
    
    <property>
      <name>dfs.blocksize</name>
      <value>134217728</value>
    </property>
    
    <property>
      <name>dfs.client.datanode-restart.timeout</name>
      <value>30</value>
    </property>
    
    <property>
      <name>dfs.client.failover.proxy.provider.hdfsCluster</name>
      <value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
    </property>
    
    <property>
      <name>dfs.client.read.shortcircuit</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.client.read.shortcircuit.streams.cache.size</name>
      <value>4096</value>
    </property>
    
    <property>
      <name>dfs.client.retry.policy.enabled</name>
      <value>false</value>
    </property>
    
    <property>
      <name>dfs.cluster.administrators</name>
      <value>hdfs hdfs</value>
    </property>
    
    <property>
      <name>dfs.content-summary.limit</name>
      <value>5000</value>
    </property>
    
    <property>
      <name>dfs.datanode.address</name>
      <value>0.0.0.0:50010</value>
    </property>
    
    <property>
      <name>dfs.datanode.balance.bandwidthPerSec</name>
      <value>6250000</value>
    </property>
    
    <property>
      <name>dfs.datanode.data.dir</name>
      <value>/data/hadoop/hdfs/data,/data1/hadoop/hdfs/data,/data2/hadoop/hdfs/data,/data3/hadoop/hdfs/data,/data4/hadoop/hdfs/data,/data5/hadoop/hdfs/data,/data6/hadoop/hdfs/data,/data7/hadoop/hdfs/data,/data8/hadoop/hdfs/data,/data9/hadoop/hdfs/data</value>
      <final>true</final>
    </property>
    
    <property>
      <name>dfs.datanode.data.dir.perm</name>
      <value>750</value>
    </property>
    
    <property>
      <name>dfs.datanode.du.reserved</name>
      <value>1073741824</value>
    </property>
    
    <property>
      <name>dfs.datanode.failed.volumes.tolerated</name>
      <value>0</value>
      <final>true</final>
    </property>
    
    <property>
      <name>dfs.datanode.handler.count</name>
      <value>512</value>
    </property>
    
    <property>
      <name>dfs.datanode.http.address</name>
      <value>0.0.0.0:50075</value>
    </property>
    
    <property>
      <name>dfs.datanode.https.address</name>
      <value>0.0.0.0:50475</value>
    </property>
    
    <property>
      <name>dfs.datanode.ipc.address</name>
      <value>0.0.0.0:8010</value>
    </property>
    
    <property>
      <name>dfs.datanode.max.transfer.threads</name>
      <value>16384</value>
    </property>
    
    <property>
      <name>dfs.datanode.max.xcievers</name>
      <value>65536</value>
    </property>
    
    <property>
      <name>dfs.domain.socket.path</name>
      <value>/var/lib/hadoop-hdfs/dn_socket</value>
    </property>
    
    <property>
      <name>dfs.encryption.key.provider.uri</name>
      <value></value>
    </property>
    
    <property>
      <name>dfs.ha.automatic-failover.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.ha.balancer.request.standby</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.ha.fencing.methods</name>
      <value>shell(/bin/true)</value>
    </property>
    
    <property>
      <name>dfs.ha.namenodes.hdfsCluster</name>
      <value>nn1,nn2</value>
    </property>
    
    <property>
      <name>dfs.heartbeat.interval</name>
      <value>3</value>
    </property>
    
    <property>
      <name>dfs.hosts.exclude</name>
      <value>/etc/hadoop/conf/dfs.exclude</value>
    </property>
    
    <property>
      <name>dfs.http.policy</name>
      <value>HTTP_ONLY</value>
    </property>
    
    <property>
      <name>dfs.https.port</name>
      <value>50470</value>
    </property>
    
    <property>
      <name>dfs.internal.nameservices</name>
      <value>hdfsCluster</value>
    </property>
    
    <property>
      <name>dfs.journalnode.edits.dir</name>
      <value>/data/hadoop/hdfs/journalnode</value>
    </property>
    
    <property>
      <name>dfs.journalnode.http-address</name>
      <value>0.0.0.0:8480</value>
    </property>
    
    <property>
      <name>dfs.journalnode.https-address</name>
      <value>0.0.0.0:8481</value>
    </property>
    
    <property>
      <name>dfs.namenode.accesstime.precision</name>
      <value>0</value>
    </property>
    
    <property>
      <name>dfs.namenode.acls.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.namenode.audit.log.async</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.namenode.avoid.read.stale.datanode</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.namenode.avoid.write.stale.datanode</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.namenode.checkpoint.dir</name>
      <value>/data/hadoop/hdfs/namesecondary</value>
    </property>
    
    <property>
      <name>dfs.namenode.checkpoint.edits.dir</name>
      <value>${dfs.namenode.checkpoint.dir}</value>
    </property>
    
    <property>
      <name>dfs.namenode.checkpoint.period</name>
      <value>21600</value>
    </property>
    
    <property>
      <name>dfs.namenode.checkpoint.txns</name>
      <value>1000000</value>
    </property>
    
    <property>
      <name>dfs.namenode.fs-limits.max-directory-items</name>
      <value>2097152</value>
    </property>
    
    <property>
      <name>dfs.namenode.fslock.fair</name>
      <value>false</value>
    </property>
    
    <property>
      <name>dfs.namenode.handler.count</name>
      <value>1024</value>
    </property>
    
    <property>
      <name>dfs.namenode.http-address.hdfsCluster.nn1</name>
      <value>tbds-100-76-17-33:50070</value>
    </property>
    
    <property>
      <name>dfs.namenode.http-address.hdfsCluster.nn2</name>
      <value>tbds-100-76-17-29:50070</value>
    </property>
    
    <property>
      <name>dfs.namenode.https-address.hdfsCluster.nn1</name>
      <value>0.0.0.0:50470</value>
    </property>
    
    <property>
      <name>dfs.namenode.https-address.hdfsCluster.nn2</name>
      <value>0.0.0.0:50470</value>
    </property>
    
    <property>
      <name>dfs.namenode.name.dir</name>
      <value>/data/hadoop/hdfs/namenode</value>
      <final>true</final>
    </property>
    
    <property>
      <name>dfs.namenode.name.dir.restore</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.namenode.rpc-address.hdfsCluster.nn1</name>
      <value>tbds-100-76-17-33:8020</value>
    </property>
    
    <property>
      <name>dfs.namenode.rpc-address.hdfsCluster.nn2</name>
      <value>tbds-100-76-17-29:8020</value>
    </property>
    
    <property>
      <name>dfs.namenode.safemode.threshold-pct</name>
      <value>0.999</value>
    </property>
    
    <property>
      <name>dfs.namenode.secondary.http-address</name>
      <value>${HDFS.SECONDARY_NAMENODE}:50090</value>
    </property>
    
    <property>
      <name>dfs.namenode.shared.edits.dir</name>
      <value>qjournal://tbds-100-76-17-32:8485;tbds-100-76-17-24:8485;tbds-100-76-17-28:8485/hdfsCluster</value>
    </property>
    
    <property>
      <name>dfs.namenode.stale.datanode.interval</name>
      <value>30000</value>
    </property>
    
    <property>
      <name>dfs.namenode.startup.delay.block.deletion.sec</name>
      <value>3600</value>
    </property>
    
    <property>
      <name>dfs.namenode.write.stale.datanode.ratio</name>
      <value>1.0f</value>
    </property>
    
    <property>
      <name>dfs.nameservices</name>
      <value>hdfsCluster</value>
    </property>
    
    <property>
      <name>dfs.permissions.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>dfs.permissions.superusergroup</name>
      <value>hdfs</value>
    </property>
    
    <property>
      <name>dfs.replication</name>
      <value>3</value>
    </property>
    
    <property>
      <name>dfs.replication.max</name>
      <value>50</value>
    </property>
    
    <property>
      <name>dfs.support.append</name>
      <value>true</value>
      <final>true</final>
    </property>
    
    <property>
      <name>dfs.webhdfs.enabled</name>
      <value>true</value>
      <final>true</final>
    </property>
    
    <property>
      <name>fs.permissions.umask-mode</name>
      <value>022</value>
    </property>
    
    <property>
      <name>ha.health-monitor.rpc-timeout.ms</name>
      <value>300000</value>
    </property>
    
    <property>
      <name>hdfs.datanode.jmx.port</name>
      <value>8701</value>
    </property>
    
    <property>
      <name>hdfs.namenode.jmx.port</name>
      <value>8700</value>
    </property>
    
    <property>
      <name>ipc.maximum.data.length</name>
      <value>268435456</value>
    </property>
    
    <property>
      <name>manage.include.files</name>
      <value>false</value>
    </property>

```

#### mapred-site.xml

```xml
# cat /usr/hdp/current/hadoop-hdfs-client/etc/hadoop/mapred-site.xml
  <configuration  xmlns:xi="http://www.w3.org/2001/XInclude">
    
    <property>
      <name>mapreduce.admin.map.child.java.opts</name>
      <value>-server -XX:NewRatio=8 -Djava.net.preferIPv4Stack=true -Dhdp.version=${hdp.version}</value>
    </property>
    
    <property>
      <name>mapreduce.admin.reduce.child.java.opts</name>
      <value>-server -XX:NewRatio=8 -Djava.net.preferIPv4Stack=true -Dhdp.version=${hdp.version}</value>
    </property>
    
    <property>
      <name>mapreduce.admin.user.env</name>
      <value>LD_LIBRARY_PATH=/usr/hdp/${hdp.version}/hadoop/lib/native:/usr/hdp/${hdp.version}/hadoop/lib/native/Linux-amd64-64:./mr-framework/hadoop/lib/native:./mr-framework/hadoop/lib/native/Linux-amd64-64</value>
    </property>
    
    <property>
      <name>mapreduce.am.max-attempts</name>
      <value>2</value>
    </property>
    
    <property>
      <name>mapreduce.application.classpath</name>
      <value>$PWD/mr-framework/hadoop/share/hadoop/mapreduce/*:$PWD/mr-framework/hadoop/share/hadoop/mapreduce/lib/*:$PWD/mr-framework/hadoop/share/hadoop/common/*:$PWD/mr-framework/hadoop/share/hadoop/common/lib/*:$PWD/mr-framework/hadoop/share/hadoop/yarn/*:$PWD/mr-framework/hadoop/share/hadoop/yarn/lib/*:$PWD/mr-framework/hadoop/share/hadoop/hdfs/*:$PWD/mr-framework/hadoop/share/hadoop/hdfs/lib/*:$PWD/mr-framework/hadoop/share/hadoop/tools/lib/*:/usr/hdp/${hdp.version}/hadoop/lib/hadoop-lzo-0.6.0.${hdp.version}.jar:/etc/hadoop/conf/secure</value>
    </property>
    
    <property>
      <name>mapreduce.application.framework.path</name>
      <value>/hdp/apps/${hdp.version}/mapreduce/mapreduce.tar.gz#mr-framework</value>
    </property>
    
    <property>
      <name>mapreduce.cluster.administrators</name>
      <value> hadoop</value>
    </property>
    
    <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
    </property>
    
    <property>
      <name>mapreduce.job.counters.max</name>
      <value>130</value>
    </property>
    
    <property>
      <name>mapreduce.job.emit-timeline-data</name>
      <value>false</value>
    </property>
    
    <property>
      <name>mapreduce.job.queuename</name>
      <value>default</value>
    </property>
    
    <property>
      <name>mapreduce.job.reduce.slowstart.completedmaps</name>
      <value>0.05</value>
    </property>
    
    <property>
      <name>mapreduce.jobhistory.address</name>
      <value>tbds-100-76-17-12:10020</value>
    </property>
    
    <property>
      <name>mapreduce.jobhistory.bind-host</name>
      <value>0.0.0.0</value>
    </property>
    
    <property>
      <name>mapreduce.jobhistory.done-dir</name>
      <value>/mr-history/done</value>
    </property>
    
    <property>
      <name>mapreduce.jobhistory.http.policy</name>
      <value>HTTP_ONLY</value>
    </property>
    
    <property>
      <name>mapreduce.jobhistory.intermediate-done-dir</name>
      <value>/mr-history/tmp</value>
    </property>
    
    <property>
      <name>mapreduce.jobhistory.webapp.address</name>
      <value>tbds-100-76-17-12:19888</value>
    </property>
    
    <property>
      <name>mapreduce.map.java.opts</name>
      <value>-Xmx15155m</value>
    </property>
    
    <property>
      <name>mapreduce.map.log.level</name>
      <value>INFO</value>
    </property>
    
    <property>
      <name>mapreduce.map.memory.mb</name>
      <value>18944</value>
    </property>
    
    <property>
      <name>mapreduce.map.output.compress</name>
      <value>false</value>
    </property>
    
    <property>
      <name>mapreduce.map.sort.spill.percent</name>
      <value>0.7</value>
    </property>
    
    <property>
      <name>mapreduce.map.speculative</name>
      <value>false</value>
    </property>
    
    <property>
      <name>mapreduce.output.fileoutputformat.compress</name>
      <value>false</value>
    </property>
    
    <property>
      <name>mapreduce.output.fileoutputformat.compress.type</name>
      <value>BLOCK</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.input.buffer.percent</name>
      <value>0.0</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.java.opts</name>
      <value>-Xmx30310m</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.log.level</name>
      <value>INFO</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.memory.mb</name>
      <value>37888</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.shuffle.fetch.retry.enabled</name>
      <value>1</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.shuffle.fetch.retry.interval-ms</name>
      <value>1000</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.shuffle.fetch.retry.timeout-ms</name>
      <value>30000</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.shuffle.input.buffer.percent</name>
      <value>0.7</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.shuffle.merge.percent</name>
      <value>0.66</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.shuffle.parallelcopies</name>
      <value>30</value>
    </property>
    
    <property>
      <name>mapreduce.reduce.speculative</name>
      <value>false</value>
    </property>
    
    <property>
      <name>mapreduce.shuffle.port</name>
      <value>13562</value>
    </property>
    
    <property>
      <name>mapreduce.task.io.sort.factor</name>
      <value>100</value>
    </property>
    
    <property>
      <name>mapreduce.task.io.sort.mb</name>
      <value>2047</value>
    </property>
    
    <property>
      <name>mapreduce.task.timeout</name>
      <value>300000</value>
    </property>
    
    <property>
      <name>yarn.app.mapreduce.am.admin-command-opts</name>
      <value>-Dhdp.version=${hdp.version}</value>
    </property>
    
    <property>
      <name>yarn.app.mapreduce.am.command-opts</name>
      <value>-Xmx15155m -Dhdp.version=${hdp.version}</value>
    </property>
    
    <property>
      <name>yarn.app.mapreduce.am.log.level</name>
      <value>INFO</value>
    </property>
    
    <property>
      <name>yarn.app.mapreduce.am.resource.mb</name>
      <value>18944</value>
    </property>
    
    <property>
      <name>yarn.app.mapreduce.am.staging-dir</name>
      <value>/user</value>
    </property>

```

#### yarn-site.xml

```xml
  <configuration  xmlns:xi="http://www.w3.org/2001/XInclude">
    
    <property>
      <name>hadoop.registry.rm.enabled</name>
      <value>false</value>
    </property>
    
    <property>
      <name>hadoop.registry.zk.quorum</name>
      <value>tbds-100-76-17-32:2181,tbds-100-76-17-21:2181,tbds-100-76-17-24:2181,tbds-100-76-17-20:2181,tbds-100-76-17-28:2181</value>
    </property>
    
    <property>
      <name>manage.include.files</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.acl.enable</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.admin.acl</name>
      <value></value>
    </property>
    
    <property>
      <name>yarn.application.classpath</name>
      <value>$HADOOP_CONF_DIR,/usr/hdp/current/hadoop-client/*,/usr/hdp/current/hadoop-client/lib/*,/usr/hdp/current/hadoop-hdfs-client/*,/usr/hdp/current/hadoop-hdfs-client/lib/*,/usr/hdp/current/hadoop-yarn-client/*,/usr/hdp/current/hadoop-yarn-client/lib/*</value>
    </property>
    
    <property>
      <name>yarn.client.nodemanager-connect.max-wait-ms</name>
      <value>60000</value>
    </property>
    
    <property>
      <name>yarn.client.nodemanager-connect.retry-interval-ms</name>
      <value>10000</value>
    </property>
    
    <property>
      <name>yarn.http.policy</name>
      <value>HTTP_ONLY</value>
    </property>
    
    <property>
      <name>yarn.log-aggregation-enable</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.log-aggregation.retain-seconds</name>
      <value>2592000</value>
    </property>
    
    <property>
      <name>yarn.log.server.url</name>
      <value>http://tbds-100-76-17-12:19888/jobhistory/logs</value>
    </property>
    
    <property>
      <name>yarn.node-labels.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.node-labels.fs-store.retry-policy-spec</name>
      <value>2000, 500</value>
    </property>
    
    <property>
      <name>yarn.node-labels.fs-store.root-dir</name>
      <value>/system/yarn/node-labels</value>
    </property>
    
    <property>
      <name>yarn.node-labels.manager-class</name>
      <value>org.apache.hadoop.yarn.server.resourcemanager.nodelabels.MemoryRMNodeLabelsManager</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.address</name>
      <value>0.0.0.0:45454</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.admin-env</name>
      <value>MALLOC_ARENA_MAX=$MALLOC_ARENA_MAX</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.aux-services</name>
      <value>mapreduce_shuffle</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
      <value>org.apache.hadoop.mapred.ShuffleHandler</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.bind-host</name>
      <value>0.0.0.0</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.container-executor.class</name>
      <value>org.apache.hadoop.yarn.server.nodemanager.DefaultContainerExecutor</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.container-monitor.interval-ms</name>
      <value>3000</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.delete.debug-delay-sec</name>
      <value>0</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-percentage</name>
      <value>90</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.disk-health-checker.min-free-space-per-disk-mb</name>
      <value>1000</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.disk-health-checker.min-healthy-disks</name>
      <value>0.25</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.health-checker.interval-ms</name>
      <value>135000</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.health-checker.script.timeout-ms</name>
      <value>60000</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.jmx.port</name>
      <value>8705</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.linux-container-executor.cgroups.hierarchy</name>
      <value>hadoop-yarn</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.linux-container-executor.cgroups.mount</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.linux-container-executor.cgroups.mount-path</name>
      <value>/cgroup</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.linux-container-executor.cgroups.strict-resource-usage</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.linux-container-executor.group</name>
      <value>hadoop</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.linux-container-executor.resources-handler.class</name>
      <value>org.apache.hadoop.yarn.server.nodemanager.util.DefaultLCEResourcesHandler</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.local-dirs</name>
      <value>/data/hadoop/yarn/log,/data1/hadoop/yarn/log,/data2/hadoop/yarn/log,/data3/hadoop/yarn/log,/data4/hadoop/yarn/log,/data5/hadoop/yarn/log,/data6/hadoop/yarn/log,/data7/hadoop/yarn/log,/data8/hadoop/yarn/log,/data9/hadoop/yarn/log</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.localizer.cache.cleanup.interval-ms</name>
      <value>600000</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.localizer.cache.target-size-mb</name>
      <value>4096</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.log-aggregation.compression-type</name>
      <value>gz</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.log-aggregation.debug-enabled</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.log-aggregation.num-log-files-per-app</name>
      <value>30</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.log-aggregation.roll-monitoring-interval-seconds</name>
      <value>-1</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.log-dirs</name>
      <value>/data/hadoop/yarn/local,/data1/hadoop/yarn/local,/data2/hadoop/yarn/local,/data3/hadoop/yarn/local,/data4/hadoop/yarn/local,/data5/hadoop/yarn/local,/data6/hadoop/yarn/local,/data7/hadoop/yarn/local,/data8/hadoop/yarn/local,/data9/hadoop/yarn/local</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.log.retain-seconds</name>
      <value>604800</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.recovery.dir</name>
      <value>/var/log/hadoop-yarn/nodemanager/recovery-state</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.recovery.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.remote-app-log-dir</name>
      <value>/app-logs</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.remote-app-log-dir-suffix</name>
      <value>logs</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.resource.cpu-vcores</name>
      <value>102</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.resource.memory-mb</name>
      <value>416768</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.resource.percentage-physical-cpu-limit</name>
      <value>80</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.vmem-check-enabled</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.nodemanager.vmem-pmem-ratio</name>
      <value>2.1</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.address</name>
      <value>tbds-100-76-17-12:8050</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.address.rm1</name>
      <value>${yarn.resourcemanager.hostname.rm1}:8032</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.address.rm2</name>
      <value>${yarn.resourcemanager.hostname.rm2}:8032</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.admin.address</name>
      <value>tbds-100-76-17-12:8141</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.am.max-attempts</name>
      <value>2</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.bind-host</name>
      <value>0.0.0.0</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.cluster-id</name>
      <value>yarn-cluster</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.connect.max-wait.ms</name>
      <value>-1</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.connect.retry-interval.ms</name>
      <value>15000</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.fs.state-store.retry-policy-spec</name>
      <value>2000, 500</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.fs.state-store.uri</name>
      <value> </value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.ha.automatic-failover.zk-base-path</name>
      <value>/yarn-leader-election</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.ha.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.ha.rm-ids</name>
      <value>rm1,rm2</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.hostname</name>
      <value>tbds-100-76-17-12</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.hostname.rm1</name>
      <value>tbds-100-76-17-12</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.hostname.rm2</name>
      <value>tbds-100-76-17-16</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.jmx.port</name>
      <value>8704</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.max-completed-applications</name>
      <value>3000</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.nodes.exclude-path</name>
      <value>/etc/hadoop/conf/yarn.exclude</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.recovery.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.resource-tracker.address</name>
      <value>tbds-100-76-17-12:8025</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.resource-tracker.address.rm1</name>
      <value>tbds-100-76-17-12:8025</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.resource-tracker.address.rm2</name>
      <value>tbds-100-76-17-16:8025</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.scheduler.address</name>
      <value>tbds-100-76-17-12:8030</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.scheduler.class</name>
      <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.fair.FairScheduler</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.scheduler.monitor.enable</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.state-store.max-completed-applications</name>
      <value>${yarn.resourcemanager.max-completed-applications}</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.store.class</name>
      <value>org.apache.hadoop.yarn.server.resourcemanager.recovery.ZKRMStateStore</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.system-metrics-publisher.dispatcher.pool-size</name>
      <value>10</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.system-metrics-publisher.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.address</name>
      <value>tbds-100-76-17-12:8084</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.address.rm1</name>
      <value>tbds-100-76-17-12:8084</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.address.rm2</name>
      <value>tbds-100-76-17-16:8084</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.delegation-token-auth-filter.enabled</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.https.address</name>
      <value>tbds-100-76-17-12:8090</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.https.address.rm1</name>
      <value>tbds-100-76-17-12:8090</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.webapp.https.address.rm2</name>
      <value>tbds-100-76-17-16:8090</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.work-preserving-recovery.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.work-preserving-recovery.scheduling-wait-ms</name>
      <value>10000</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.zk-acl</name>
      <value>world:anyone:rwcda</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.zk-address</name>
      <value>tbds-100-76-17-32:2181,tbds-100-76-17-21:2181,tbds-100-76-17-24:2181,tbds-100-76-17-20:2181,tbds-100-76-17-28:2181</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.zk-num-retries</name>
      <value>1000</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.zk-retry-interval-ms</name>
      <value>1000</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.zk-state-store.parent-path</name>
      <value>/rmstore</value>
    </property>
    
    <property>
      <name>yarn.resourcemanager.zk-timeout-ms</name>
      <value>10000</value>
    </property>
    
    <property>
      <name>yarn.scheduler.fair.allow-undeclared-pools</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.scheduler.fair.preemption</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.scheduler.fair.preemption.cluster-utilization-threshold</name>
      <value>0.8</value>
    </property>
    
    <property>
      <name>yarn.scheduler.fair.user-as-default-queue</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.scheduler.maximum-allocation-mb</name>
      <value>416768</value>
    </property>
    
    <property>
      <name>yarn.scheduler.maximum-allocation-vcores</name>
      <value>102</value>
    </property>
    
    <property>
      <name>yarn.scheduler.minimum-allocation-mb</name>
      <value>512</value>
    </property>
    
    <property>
      <name>yarn.scheduler.minimum-allocation-vcores</name>
      <value>1</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.address</name>
      <value>tbds-100-76-17-28:10200</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.bind-host</name>
      <value>0.0.0.0</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.client.max-retries</name>
      <value>30</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.client.retry-interval-ms</name>
      <value>1000</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.enabled</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.generic-application-history.store-class</name>
      <value>org.apache.hadoop.yarn.server.applicationhistoryservice.NullApplicationHistoryStore</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.http-authentication.proxyuser.root.groups</name>
      <value>*</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.http-authentication.proxyuser.root.hosts</name>
      <value>tbds-100-76-17-4</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.http-authentication.simple.anonymous.allowed</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.http-authentication.type</name>
      <value>simple</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.leveldb-state-store.path</name>
      <value>/data/hadoop/yarn/timeline</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.leveldb-timeline-store.path</name>
      <value>/data/hadoop/yarn/timeline</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.leveldb-timeline-store.read-cache-size</name>
      <value>104857600</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.leveldb-timeline-store.start-time-read-cache-size</name>
      <value>10000</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.leveldb-timeline-store.start-time-write-cache-size</name>
      <value>10000</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.leveldb-timeline-store.ttl-interval-ms</name>
      <value>300000</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.recovery.enabled</name>
      <value>false</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.state-store-class</name>
      <value>org.apache.hadoop.yarn.server.timeline.recovery.LeveldbTimelineStateStore</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.store-class</name>
      <value>org.apache.hadoop.yarn.server.timeline.LeveldbTimelineStore</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.ttl-enable</name>
      <value>true</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.ttl-ms</name>
      <value>2678400000</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.webapp.address</name>
      <value>tbds-100-76-17-28:8188</value>
    </property>
    
    <property>
      <name>yarn.timeline-service.webapp.https.address</name>
      <value>tbds-100-76-17-28:8190</value>
    </property>

```

#### log4j.properties

```shell
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

