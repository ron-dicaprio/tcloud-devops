## 以两个mysql5.7的docker容器为例为例搭建主从
> DB-Master:主机10.0.8.15
> DB-Slave :备机10.0.8.16

## 安装mysql客户端
```sh
# yum install mysql -y
```
## 拉起DB-Master和DB-Slave:
```sh
# docker run --name DB-Master --restart=always --net=DB-bridge -d -p 53306:3306 -e TZ="Asia/Shanghai" -e MYSQL_ROOT_PASSWORD=@Sysadm1n -v /data/mysql_1/data:/var/lib/mysql mysql:5.7

# docker run --name DB-Slave  --restart=always --net=DB-bridge -d -p 53307:3306 -e TZ="Asia/Shanghai" -e MYSQL_ROOT_PASSWORD=@Sysadm1n -v /data/mysql_2/data:/var/lib/mysql mysql:5.7
```

## 修改主服务器配置
### 修改my.cnf,
log_bin=mysql
server_id=100
sed -i '29a log_bin=mysql' /etc/mysql/mysql.conf.d/mysqld.cnf
sed -i '29a server_id=100' /etc/mysql/mysql.conf.d/mysqld.cnf
sed -i '29a sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' /etc/mysql/mysql.conf.d/mysqld.cnf
docker中位于/etc/mysql/mysql.conf.d/mysqld.cnf
```yaml
# cat /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
log_bin=mysql
server_id=100
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
binlog_cache_size = 32K
thread_stack = 256K
join_buffer_size = 256K
query_cache_type = 0
max_heap_table_size = 128M
lower_case_table_names = 1
port = 3306
default_storage_engine = InnoDB
performance_schema_max_table_instances = 400
table_definition_cache = 400
skip-external-locking
key_buffer_size = 256M
table_open_cache = 1024
sort_buffer_size = 4096K
net_buffer_length = 4K
read_buffer_size = 4096K
read_rnd_buffer_size = 256K
myisam_sort_buffer_size = 64M
thread_cache_size = 128
query_cache_size = 0M
tmp_table_size = 128M
explicit_defaults_for_timestamp = true
#skip-name-resolve
max_connections = 500
max_connect_errors = 100
open_files_limit = 65535
skip-ssl
log_bin = ON
sync_binlog = 1
binlog_format = ROW
expire-logs-days=10
binlog-ignore-db = mysql
binlog_ignore_db = information_schema
binlog_ignore_db = performation_schema
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
```
## 创建从节点的访问账号
CREATE USER 'slave'@'%' IDENTIFIED BY '@Sysadm1n';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'slave'@'%';

## 查看master状态
```sql
show master status;
mysql> show master status;
+--------------+----------+--------------+------------------+-------------------+
| File         | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+--------------+----------+--------------+------------------+-------------------+
| mysql.000001 |      609 |              |                  |                   |
+--------------+----------+--------------+------------------+-------------------+
1 row in set
```

## 修改从服务器配置
### 修改my.cnf
server_id=101
sed -i '29a server_id=101' /etc/mysql/mysql.conf.d/mysqld.cnf
docker中位于/etc/mysql/mysql.conf.d/mysqld.cnf
```yaml
# cat /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
server_id=101
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
binlog_cache_size = 32K
thread_stack = 256K
join_buffer_size = 256K
query_cache_type = 0
max_heap_table_size = 128M
lower_case_table_names = 1
port = 3306
default_storage_engine = InnoDB
performance_schema_max_table_instances = 400
table_definition_cache = 400
skip-external-locking
key_buffer_size = 256M
table_open_cache = 1024
sort_buffer_size = 4096K
net_buffer_length = 4K
read_buffer_size = 4096K
read_rnd_buffer_size = 256K
myisam_sort_buffer_size = 64M
thread_cache_size = 128
query_cache_size = 0M
tmp_table_size = 128M
explicit_defaults_for_timestamp = true
#skip-name-resolve
max_connections = 500
max_connect_errors = 100
open_files_limit = 65535
skip-ssl
log_bin = ON
sync_binlog = 1
binlog_format = ROW
expire-logs-days=10
binlog-ignore-db = mysql
binlog_ignore_db = information_schema
binlog_ignore_db = performation_schema
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
```
## 设置主节点
CHANGE MASTER TO MASTER_HOST='10.0.8.15',MASTER_PORT=53306,MASTER_USER='slave',MASTER_PASSWORD='@Sysadm1n',MASTER_LOG_FILE='mysql.000001',MASTER_LOG_POS=609;

## 开启主从同步并查看从节点日志
start slave;

show slave status;


## 推荐mysqld配置文件
```yaml
[mysqld]
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
binlog_cache_size = 32K
thread_stack = 256K
join_buffer_size = 256K
query_cache_type = 0
max_heap_table_size = 128M
lower_case_table_names = 1
port = 3306
default_storage_engine = InnoDB
performance_schema_max_table_instances = 400
table_definition_cache = 400
skip-external-locking
key_buffer_size = 256M
table_open_cache = 1024
sort_buffer_size = 4096K
net_buffer_length = 4K
read_buffer_size = 4096K
read_rnd_buffer_size = 256K
myisam_sort_buffer_size = 64M
thread_cache_size = 128
query_cache_size = 0M
tmp_table_size = 128M


explicit_defaults_for_timestamp = true
#skip-name-resolve
max_connections = 500
max_connect_errors = 100
open_files_limit = 65535


skip-ssl


log_bin = ON
server_id = 2
sync_binlog = 1
binlog_format = ROW
expire-logs-days=10
binlog-ignore-db = mysql
binlog_ignore_db = information_schema
binlog_ignore_db = performation_schema


# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
```
## 内容解读：
sql_mode：设置MySQL的SQL模式，这里指定了一系列严格模式和错误处理模式，例如禁止日期字段中的零值、禁止自动创建用户等。
binlog_cache_size：指定了二进制日志缓存的大小，这是MySQL服务器用于存储二进制日志事件的缓冲区大小。
thread_stack：设置线程栈的大小，即每个MySQL线程的栈空间大小。
join_buffer_size：设置连接缓冲区的大小，用于执行连接操作时的中间结果缓存。
query_cache_type：设置查询缓存的类型，这里将其设置为0，表示禁用查询缓存。
max_heap_table_size：设置最大的堆表（内存表）大小限制。
lower_case_table_names：设置表名的大小写规则，这里设置为1表示表名不区分大小写。
port：指定MySQL服务器监听的端口号。
default_storage_engine：设置默认的存储引擎，这里设置为InnoDB。
performance_schema_max_table_instances：设置性能模式中表实例的最大数量。
table_definition_cache：设置表定义缓存的大小。
skip-external-locking：禁用外部锁定，不再支持旧式的外部锁定。
key_buffer_size：设置MyISAM索引缓冲区的大小。
table_open_cache：设置表打开缓存的大小，用于存储表的打开实例。
sort_buffer_size：设置排序缓冲区的大小，用于执行排序操作时的中间结果缓存。
net_buffer_length、read_buffer_size、read_rnd_buffer_size：分别设置网络缓冲区、读取缓冲区和随机读取缓冲区的大小。
myisam_sort_buffer_size：设置MyISAM排序缓冲区的大小。
thread_cache_size：设置线程缓存的大小，用于存储已经分配但未被使用的线程。
query_cache_size：设置查询缓存的大小，这里将其设置为0，表示禁用查询缓存。
tmp_table_size：设置临时表的最大大小。
explicit_defaults_for_timestamp：设置是否启用了显式的时间戳默认值。
max_connections：设置最大连接数。
max_connect_errors：设置最大连接错误数。
open_files_limit：设置打开文件的限制数。
skip-ssl：禁用SSL连接。
log_bin：启用二进制日志功能。
server_id：设置服务器的ID。
sync_binlog：设置二进制日志的同步方式。
binlog_format：设置二进制日志的格式，这里设置为ROW格式。
expire-logs-days：设置二进制日志文件的过期时间。
binlog-ignore-db：设置要忽略的数据库，这里分别忽略了mysql、information_schema和performance_schema数据库。
symbolic-links：设置是否允许符号链接，这里设置为0，禁用符号链接以防止安全风险。
