
import uvicorn,logging,pymysql,uuid
from fastapi import FastAPI,Request
from logging.handlers import RotatingFileHandler
from fastapi.responses import FileResponse
from dbutils.pooled_db import PooledDB

MysqlPOOL=None
def init_pool():
    # 配置数据库连接信息
    if MysqlPOOL is None:
        MysqlPOOL = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=20,  # 连接池允许的最大连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接
            maxcached=10,  # 链接池中最多闲置的链接
            maxshared=6,  # 链接池中最多共享的链接数量
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待
            host='118.118.118.118',  # 数据库服务器地址
            port=3306,  # 数据库服务器端口
            user='root',  # 数据库用户名
            password='password',  # 数据库密码
            database='registry',  # 数据库名
            charset='utf8mb4'  # 数据库编码
        )
        return MysqlPOOL
    
def setup_logger(log_file='app.log', backup_count=None, max_bytes=None):
    """设置日志记录器并返回日志记录器对象"""
    # 如果未定义日志大小默认10M
    max_bytes=max_bytes if max_bytes else 10485760
    # 如果未定义保存天数默认7天
    backup_count=backup_count if backup_count else 7
    # 创建或获取一个日志记录器
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # 创建一个 RotatingFileHandler 对象，用于将日志记录到文件，并限制文件大小
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # 将文件处理程序添加到日志记录器中
    logger.addHandler(file_handler)
    return logger

# 初始化日志对象
logger=setup_logger()

# todo:防止SQL注入
def run_strsql(str_sql):
    # 从数据库连接池中获取连接
    init_pool()
    # 使用连接池获取连接
    try:
        with MysqlPOOL.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(str_sql)
                result = cursor.fetchall()
                conn.commit()
        return result
    except Exception as Err:
        logger.error("Error updating order:",Err)
        # 抛出异常供上层处理
        raise

# 初始化API实例对象
app=FastAPI()

# 定义首页
@app.get("/")
async def html():
    return FileResponse("./index.html")

def UpdateTelList():
    tel_res=run_strsql("select consignee_tel from order_info;")
    tel_list=[tel_res[i][0] for i in range(0,len(tel_res))]
    return tel_list

tel_list=UpdateTelList()

# 根据电话号码获取订单号
@app.get(path="/GetOrderInfo/{usertel}")
async def GetOrderInfo(usertel:str,page=1, page_size=10):
    if usertel in tel_list:
        # 分页查询，避免一次性获取大量数据
        # offset = (page - 1) * page_size
        # user_list=run_strsql("select out_trade_no from order_info where consignee_tel = %s LIMIT %s OFFSET %s;" % (usertel,page_size, offset))
        user_list=run_strsql("select out_trade_no from order_info where consignee_tel = %s;" % (usertel))  
        logger.info({"code": 200,"data":[{"usertel": usertel, "trade_no":user_list[0][0]}]})
        return {"code": 200,"data":[{"usertel": usertel, "trade_no":user_list[0][0]}]}
    else:
        logger.info({"code": 500, "data":[{"message": "usertel error!"}]})
        return {"code": 500, "data":[{"message": "usertel error!"}]}

# 新增一个POST接口并定义参数
@app.post("/UpdateOrder")
async def UpdateOrder(request: Request):
    global tel_list
    try:
        data = await request.json()
        trade_no = data.get('trade_no')
        newtel = data.get('newtel')
        # 假设成功创建订单，返回订单信息
        str_sql="update order_info set consignee_tel='%s' where out_trade_no='%s';" % (newtel,trade_no)
        logger.info(str_sql)
        res=run_strsql(str_sql)
        tel_list=UpdateTelList()
        return {"code": 200, "data":[{"message": res}]}
    except Exception as Err:
        logger.error(Err)
        return {"code": 500, "data":[{"message": "data error!"}]}

if __name__=="__main__":
    uvicorn.run("pyfastapi:app", port=8080, reload=True)
