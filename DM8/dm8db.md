# DM8 info Collector

## DM8DB for Docker 

### Pull a dm8 docker image

```shell
# docker pull registry.cn-guangzhou.aliyuncs.com/x86-registry/dm8:dm8_20241230_rev255012_x86_rh6_64
```

### Run docker container

```shell
# docker run -d -p 55236:5236 --name dm8db \
--restart=always --privileged=true \
-e LD_LIBRARY_PATH=/opt/dmdbms/bin \
-e PAGE_SIZE=32 \
-e EXTENT_SIZE=32 \
-e LOG_SIZE=2048 \
-e UNICODE_FLAG=1 \
-e INSTANCE_NAME=DMSERVER \
-e SYSDBA_PWD=Sysadm1n \
-v /data/dmdbms/data:/opt/dmdbms/data \
dm8:dm8_20241230_rev255012_x86_rh6_64
```

### deploy_dm8.yaml

```yml
version: '3.8'
services:
  dm8db:
    image: dm8:dm8_20241230_rev255012_x86_rh6_64
    container_name: dm8db
    restart: always
    privileged: true
    environment:
      - LD_LIBRARY_PATH=/opt/dmdbms/bin
      - PAGE_SIZE=32
      - EXTENT_SIZE=32
      - LOG_SIZE=2048
      - UNICODE_FLAG=1
      - INSTANCE_NAME=DMSERVER
      - SYSDBA_PWD=Sysadm1n
    ports:
      - "55236:5236"
    volumes:
      - /data/dmdbms/data:/opt/dmdbms/data
```

### config info

| 参数           | 描述                                              | 备注           |
| -------------- | ------------------------------------------------- | -------------- |
| PAGE_SIZE      | 页大小，可选值 4/8/16/32，默认值：8               | 设置后不可修改 |
| EXTENT_SIZE    | 簇大小，可选值 16/32/64，默认值：16               | 设置后不可修改 |
| CASE_SENSITIVE | 1:大小写敏感；0：大小写不敏感，默认值：1          | 设置后不可修改 |
| UNICODE_FLAG   | 字符集选项；0:GB18030;1:UTF-8;2:EUC-KR，默认值：0 | 设置后不可修改 |
| INSTANCE_NAME  | 初始化数据库实例名字，默认值：DAMENG              | 可修改         |
| SYSDBA_PWD     | 初始化实例时设置 SYSDBA 的密码                    | 可修改         |
| BLANK_PAD_MODE | 空格填充模式，默认值：0                           | 设置后不可修改 |
| LOG_SIZE       | 日志文件大小，单位为：M，默认值：256              | 可修改         |
| BUFFER         | 系统缓存大小，单位为：M，默认值：1000             | 可修改         |

> **注意**
>
> 1.SYSDBA_PWD 预设的时候，密码长度为 9~48 个字符，docker 版本使用暂不支持特殊字符为密码
> 2.强烈建议用户在首次安装数据库初始化实例时，立即修改数据库系统用户的初始密码，并设置一定的密码强度，以保障数据安全性。
> 3.-e 设置的时候 初始化参数必须使用大写，不可使用小写。

### Conn dm8db

```shell
# docker exec -it dm8db bash
root@4d2c5b325df9:/# /opt/dmdbms/bin/disql SYSDBA/Sysadm1n

Server[LOCALHOST:5236]:mode is normal, state is open
login used time : 2.700(ms)
disql V8
SQL> select * from v$instance;
```

### SQL Command

```sql
-- 查看实例信息
select * from v$instance;
-- 查看当前用户
select user from dual;
-- 创建用户及密码
create user dm8dba identified by "dm8dba@123";
-- 修改用户密码
alter user dm8dba identified by Sysadm1n;
-- 授权用户
grant public,resource,DBA to dm8dba WITH ADMIN OPTION ;
-- 取消DBA权限
revoke DBA from dm8dba;
-- 查看角色
select role from dba_roles;
-- 查看dm8dba用户信息
select * from dba_users where username='dm8dba';
-- 查看dm8dba用户权限
select * from dba_role_privs where grantee='dm8dba';
```

## DM8DB for Linux

### Install dmdb8

```shell
# id 1000
uid=1000(dmdba) gid=1000(dinstall) groups=1000(dinstall)
# groupadd dinstall -g 1000
# useradd -g dinstall -m -d /home/dmdba -s /bin/bash -u 1000 dmdba
# passwd dmdba
```

```shell
# vim /etc/security/limits.conf
dmdba  soft      nice       0
dmdba  hard      nice       0
dmdba  soft      as         unlimited
dmdba  hard      as         unlimited
dmdba  soft      fsize      unlimited
dmdba  hard      fsize      unlimited
dmdba  soft      nproc      65536
dmdba  hard      nproc      65536
dmdba  soft      nofile     65536
dmdba  hard      nofile     65536
dmdba  soft      core       unlimited
dmdba  hard      core       unlimited
dmdba  soft      data       unlimited
dmdba  hard      data       unlimited
```

```shell
# su - dmdba
$ ulimit -a
```

```shell
##实例保存目录
mkdir -p /dmdata/data 
##归档保存目录
mkdir -p /dmdata/arch
##备份保存目录
mkdir -p /dmdata/dmbak
chown -R dmdba:dinstall /dmdata/data
chown -R dmdba:dinstall /dmdata/arch
chown -R dmdba:dinstall /dmdata/dmbak
chmod -R 755 /dmdata/data
chmod -R 755 /dmdata/arch
chmod -R 755 /dmdata/dmbak
```

```shell
# mount -o loop dm8_20240116_x86_rh7_64.iso /mnt
# su - dmdba
$ /mnt/DMInstall.bin -i
# /home/dmdba/dmdbms/script/root/root_installer.sh
```

```shell
# su - dmdba
$ cd /home/dmdba/dmdbms/bin
$ ./dminit path=/dmdata/data PAGE_SIZE=32 EXTENT_SIZE=32 CASE_SENSITIVE=y
CHARSET=1 DB_NAME=DMTEST INSTANCE_NAME=DBSERVER PORT_NUM=5237 SYSDBA_PWD=Sysadm1n  SYSAUDITOR_PWD=Sysadm1n
```

```shell

exit 0
```
