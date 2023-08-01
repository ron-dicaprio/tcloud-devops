#-*- coding:utf-8 -*-
import json,easygui,sys
from configparser import ConfigParser
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tsf.v20180326 import tsf_client, models

'''
---写一点废话---
一个功能一个函数,既然是基于腾讯的SDK就先不混着写了
通过easygui实现简单的选择和传参
后续可以考虑用PyQt5来二次改写功能页
我开始搭建屎山
代码很丑陋
不接受批评
'''

def config_init():
    # 全局变量
    global secret_id,secret_key,tsf_endpoint,tce_region,app_list
    try:
        config = ConfigParser() 
        # 配置文件带中文,定义编码方式
        config.read("init_tce.ini",encoding='utf-8')
        # secret id和key
        secret_id=config.get("tce_config", "secret_id") 
        secret_key=config.get("tce_config", "secret_key") 
        # tsf_endpoint
        tsf_endpoint=config.get("tce_config", "tsf_endpoint")
        # 区域码
        tce_region=config.get("tce_config", "tce_region")
        # 应用名称  string转list类型
        app_list=config.get("tce_config", "app_list").split(',')
        print('配置文件解析完毕')
    except Exception as err:
        print('配置文件解析失败，请确认\n',err)
        sys.exit(-1)

# 创建微服务应用
def tsf_CreateApplication(self):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        cred = credential.Credential(secret_id, secret_key)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        httpProfile.endpoint = tsf_endpoint
        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"  # 指定展示英文（默认为中文）
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.CreateApplicationRequest()

        params = {
            # 应用名称
            "ApplicationName": self,
            # 应用类别
            "ApplicationType": "C",
            # 微服务类别
            "MicroserviceType": "N"
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个CreateApplicationResponse的实例，与请求对象对应
        resp = client.CreateApplication(req)
        # 输出json格式的字符串回包
        return resp.to_json_string()
        # {"Result": "application-yd9rm45a", "RequestId": "e1bf32f7-7fe0-49da-bc19-0469650fcbcd"}
    except TencentCloudSDKException as err:
        return err

def get_all_config():
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        #cred = credential.Credential("SecretId", "SecretKey")
        cred = credential.Credential(secret_id, secret_key)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        httpProfile.endpoint = tsf_endpoint

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeConfigsRequest()
        
        # 不传参数,默认返回所有应用的配置
        params = {

        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeConfigsResponse的实例，与请求对象对应
        resp = client.DescribeConfigs(req)
        # 输出json格式的字符串回包
        return resp.to_json_string()

    except TencentCloudSDKException as err:
        return err

if __name__=="__main__":
    config_init()
    func_choice=easygui.choicebox(title="腾讯云TSF接口调用工具V0.1",msg="请选择以下相应的功能",choices=["创建集群微服务应用","获取集群配置文件","获取集群镜像版本号"])
    if func_choice=='创建集群微服务应用':
        str_text=[]
        for i in range(0,len(app_list)):
            #print(app_list[i])
            # .strip()处理下字符前后空格
            str_text.append(str(tsf_CreateApplication(app_list[i].strip()))+'\n')
        easygui.codebox(title="腾讯云TSF接口调用工具V0.1",msg="TSF接口调用结果如下:",text=str_text)

    elif func_choice=='获取集群配置文件':
        # 格式化json对象
        str_json=json.dumps(json.loads(get_all_config()),indent=4)
        easygui.codebox(title="腾讯云TSF接口调用工具V0.1",msg="TSF接口调用结果如下:",text=str_json)

    elif func_choice=='获取集群镜像版本号':
        print('todo list')
    else:
        print("选择错误,请确认!")
        sys.exit(-1)
