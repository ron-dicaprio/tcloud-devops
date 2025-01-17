#-*- coding:utf-8 -*-
import dmPython
from dbutils.pooled_db import PooledDB
POOL = PooledDB(
 creator=dmPython, # 使用链接数据库的模块
 maxconnections=6, # 连接池允许的最大连接数，0 和 None 表示不限制连接数
 mincached=2, # 初始化时，链接池中至少创建的空闲的链接，0 表示不创建
 maxcached=5, # 链接池中最多闲置的链接，0 和 None 不限制
 maxshared=3, # 链接池中最多共享的链接数量，0 和 None 表示全部共享 
 blocking=True, # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
 maxusage=None, # 一个链接最多被重复使用的次数，None 表示无限制
 setsession=[], # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
 ping=0,
 # pingDM 服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 7 = always
 host='1.1.1.1', # 主机号
 port=55236, # 端口号
 user='SYSDBA', # 用户名
 password='SYSDBA', # 密码
)

def PyDm8sql_with_pool(str_sql):
    try:
        conn = POOL.connection()
        with conn.cursor() as cursor:
            cursor.execute(str_sql)
            conn.commit()
            return cursor.fetchall()
    except Exception as err:
        print(f"Error occurred: {err}")
        return err
    finally:
        # 将连接返回给连接池
        conn.close()

print(PyDm8sql_with_pool("select * from v$instance"))
