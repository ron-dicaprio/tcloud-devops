#-*- coding:utf-8 -*-
import json,sys
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tsf.v20180326 import tsf_client, models

# 生产及预生产都是通过AKSK判定，禁止弄错
SecretId='AKIDb5ObdR1NUN1WtLm9QUM0SjoZ6Pi8VxHU'
SecretKey='CGG553DF5iFcnlZHxY3UsCWmAa2iNByw'
tce_region='ap-guangzhou'
tce_endpoint='tsf.tencentcloudapi.com'

app_list_nw=["yyzx-ctrl-jd",
    "yyzx-service",
    "cxssb-front-jd-web",
    "xwcjsjjg-service",
    "yyzx-front-jd-web",
    "cxssb-ctrl-jd",
    "cxssb-service",
    "dksq-ctrl-jd",
    "dksq-service",
    "dksq-front-jd-web",
    "jcaj-front-jd-web",
    "jcaj-service",
    "jcaj-ctrl-jd",
    "j3cx-service",
    "jcsb-service",
    "mh-ctrl-jd",
    "mh-service-jd",
    "mh-service",
    "mh-front-jd-web",
    "nsrxx-service",
    "skzs-ctrl-jd",
    "skzs-service",
    "skzs-front-jd-web",
    "sqsp-service",
    "wfcz-service",
    "wfwwg-service",
    "xxzx-ctrl-jd",
    "xxzxnsrd-service",
    "xxzxjd-service",
    "xxzx-front-jd-web",
    "ztxxbg-ctrl-jd",
    "ztxxbg-service",
    "ztxxbg-front-jd-web",
    "ztzx-ctrl-jd",
    "ztzx-service",
    "ztzx-front-jd-web"]

app_list_ww=["xwcjsjjs-ctrl-nsrd",
    "cxssb-ctrl-nsrd",
    "cxssb-front-nsrd-web",
    "dksq-ctrl-nsrd",
    "dksq-front-nsrd-web",
    "jcaj-front-nsrd-web",
    "jcaj-ctrl-nsrd",
    "mh-ctrl-nsrd",
    "mh-front-nsrd-web",
    "skzs-ctrl-nsrd",
    "skzs-front-nsrd-web",
    "xxzx-ctrl-nsrd",
    "xxzx-front-nsrd-web",
    "ztxxbg-ctrl-nsrd",
    "ztxxbg-front-nsrd-web",
    "ztzx-ctrl-nsrd",
    "ztzx-front-nsrd-web"]

# 创建docker微服务应用-yscsj
def tsf_CreateApplication(self):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.protocol = "http"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        httpProfile.endpoint = tce_endpoint
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

# 获取应用的applicationID,此ID不同于部署组ID
def get_applicationID_list(self):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.protocol = "http"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        httpProfile.endpoint = tce_endpoint

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.DescribeApplicationsRequest()
        params = {
            "SearchWord": self
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个DescribeApplicationsResponse的实例，与请求对象对应
        resp = client.DescribeApplications(req)
        # 输出json格式的字符串回包
        str_json=json.loads(resp.to_json_string())
        applicationlist=[]
        for i in range(0,len(str_json["Result"]["Content"])):
            applicationlist.append(str_json["Result"]["Content"][i]["ApplicationId"])
        return applicationlist[0]

    except TencentCloudSDKException as err:
        return err

def tsf_CreateGroup(self):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)

        req = models.CreateGroupRequest()
        ApplicationId=get_applicationID_list(self)
        params = {
            "ApplicationId": ApplicationId,
            "GroupName": self,
            "NamespaceId": "namespace-byxg54vl",
            "ClusterId": "cls-8wnh66qm"
          }
        req.from_json_string(json.dumps(params))

        resp = client.CreateGroup(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def get_GroupID(self):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)

        req = models.DescribeSimpleGroupsRequest()
        params = {
            "SearchWord": self
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeSimpleGroups(req)
        return json.loads(resp.to_json_string())['Result']['Content'][0]['GroupId']
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)


def tsf_DescribeTaskRecords(self):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)

        req = models.DescribeTaskRecordsRequest()
        params = {
            "SearchWord": self
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeTaskRecords(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)


# 基础申报重试处理
def tsf_CreateTask_JcsbRetryTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 240000,
            "TaskName": "基础申报重试处理",
            "TaskContent": "cn.gov.chinatax.gt4.jcsb.task.JcsbRetryTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "FixRate",
              "RepeatInterval": 300000
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "ShardCount": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-jcsb-service'),
            "TaskArgument": "4"
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)



# 增值税留抵抵欠
def tsf_CreateTask_ZzslddqTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 1800000,
            "TaskName": "增值税留抵抵欠",
            "TaskContent": "cn.gov.chinatax.gt4.dsrw.zzslddq.ZzslddqTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 0 2 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "ShardCount": 202,
            "ShardArguments": [
          {
            "ShardKey": 1,
            "ShardValue": "11301020000"
          },
          {
            "ShardKey": 2,
            "ShardValue": "11301040000"
          },
          {
            "ShardKey": 3,
            "ShardValue": "11301050000"
          },
          {
            "ShardKey": 4,
            "ShardValue": "11301070000"
          },
          {
            "ShardKey": 5,
            "ShardValue": "11301080000"
          },
          {
            "ShardKey": 6,
            "ShardValue": "11301090000"
          },
          {
            "ShardKey": 7,
            "ShardValue": "11301100000"
          },
          {
            "ShardKey": 8,
            "ShardValue": "11301110000"
          },
          {
            "ShardKey": 9,
            "ShardValue": "11301210000"
          },
          {
            "ShardKey": 10,
            "ShardValue": "11301230000"
          },
          {
            "ShardKey": 11,
            "ShardValue": "11301250000"
          },
          {
            "ShardKey": 12,
            "ShardValue": "11301260000"
          },
          {
            "ShardKey": 13,
            "ShardValue": "11301270000"
          },
          {
            "ShardKey": 14,
            "ShardValue": "11301280000"
          },
          {
            "ShardKey": 15,
            "ShardValue": "11301290000"
          },
          {
            "ShardKey": 16,
            "ShardValue": "11301300000"
          },
          {
            "ShardKey": 17,
            "ShardValue": "11301310000"
          },
          {
            "ShardKey": 18,
            "ShardValue": "11301320000"
          },
          {
            "ShardKey": 19,
            "ShardValue": "11301330000"
          },
          {
            "ShardKey": 20,
            "ShardValue": "11301810000"
          },
          {
            "ShardKey": 21,
            "ShardValue": "11301830000"
          },
          {
            "ShardKey": 22,
            "ShardValue": "11301840000"
          },
          {
            "ShardKey": 23,
            "ShardValue": "11301900000"
          },
          {
            "ShardKey": 24,
            "ShardValue": "11301910000"
          },
          {
            "ShardKey": 25,
            "ShardValue": "11301920000"
          },
          {
            "ShardKey": 26,
            "ShardValue": "11301940000"
          },
          {
            "ShardKey": 27,
            "ShardValue": "11302020000"
          },
          {
            "ShardKey": 28,
            "ShardValue": "11302030000"
          },
          {
            "ShardKey": 29,
            "ShardValue": "11302040000"
          },
          {
            "ShardKey": 30,
            "ShardValue": "11302050000"
          },
          {
            "ShardKey": 31,
            "ShardValue": "11302070000"
          },
          {
            "ShardKey": 32,
            "ShardValue": "11302080000"
          },
          {
            "ShardKey": 33,
            "ShardValue": "11302090000"
          },
          {
            "ShardKey": 34,
            "ShardValue": "11302230000"
          },
          {
            "ShardKey": 35,
            "ShardValue": "11302240000"
          },
          {
            "ShardKey": 36,
            "ShardValue": "11302250000"
          },
          {
            "ShardKey": 37,
            "ShardValue": "11302270000"
          },
          {
            "ShardKey": 38,
            "ShardValue": "11302290000"
          },
          {
            "ShardKey": 39,
            "ShardValue": "11302810000"
          },
          {
            "ShardKey": 40,
            "ShardValue": "11302830000"
          },
          {
            "ShardKey": 41,
            "ShardValue": "11302900000"
          },
          {
            "ShardKey": 42,
            "ShardValue": "11302910000"
          },
          {
            "ShardKey": 43,
            "ShardValue": "11302930000"
          },
          {
            "ShardKey": 44,
            "ShardValue": "11302940000"
          },
          {
            "ShardKey": 45,
            "ShardValue": "11302950000"
          },
          {
            "ShardKey": 46,
            "ShardValue": "11302960000"
          },
          {
            "ShardKey": 47,
            "ShardValue": "11303020000"
          },
          {
            "ShardKey": 48,
            "ShardValue": "11303030000"
          },
          {
            "ShardKey": 49,
            "ShardValue": "11303040000"
          },
          {
            "ShardKey": 50,
            "ShardValue": "11303210000"
          },
          {
            "ShardKey": 51,
            "ShardValue": "11303220000"
          },
          {
            "ShardKey": 52,
            "ShardValue": "11303230000"
          },
          {
            "ShardKey": 53,
            "ShardValue": "11303240000"
          },
          {
            "ShardKey": 54,
            "ShardValue": "11303900000"
          },
          {
            "ShardKey": 55,
            "ShardValue": "11303930000"
          },
          {
            "ShardKey": 56,
            "ShardValue": "11304020000"
          },
          {
            "ShardKey": 57,
            "ShardValue": "11304030000"
          },
          {
            "ShardKey": 58,
            "ShardValue": "11304040000"
          },
          {
            "ShardKey": 59,
            "ShardValue": "11304060000"
          },
          {
            "ShardKey": 60,
            "ShardValue": "11304230000"
          },
          {
            "ShardKey": 61,
            "ShardValue": "11304240000"
          },
          {
            "ShardKey": 62,
            "ShardValue": "11304250000"
          },
          {
            "ShardKey": 63,
            "ShardValue": "11304260000"
          },
          {
            "ShardKey": 64,
            "ShardValue": "11304270000"
          },
          {
            "ShardKey": 65,
            "ShardValue": "11304280000"
          },
          {
            "ShardKey": 66,
            "ShardValue": "11304290000"
          },
          {
            "ShardKey": 67,
            "ShardValue": "11304300000"
          },
          {
            "ShardKey": 68,
            "ShardValue": "11304310000"
          },
          {
            "ShardKey": 69,
            "ShardValue": "11304320000"
          },
          {
            "ShardKey": 70,
            "ShardValue": "11304330000"
          },
          {
            "ShardKey": 71,
            "ShardValue": "11304340000"
          },
          {
            "ShardKey": 72,
            "ShardValue": "11304350000"
          },
          {
            "ShardKey": 73,
            "ShardValue": "11304810000"
          },
          {
            "ShardKey": 74,
            "ShardValue": "11304900000"
          },
          {
            "ShardKey": 75,
            "ShardValue": "11304910000"
          },
          {
            "ShardKey": 76,
            "ShardValue": "11305020000"
          },
          {
            "ShardKey": 77,
            "ShardValue": "11305030000"
          },
          {
            "ShardKey": 78,
            "ShardValue": "11305210000"
          },
          {
            "ShardKey": 79,
            "ShardValue": "11305220000"
          },
          {
            "ShardKey": 80,
            "ShardValue": "11305230000"
          },
          {
            "ShardKey": 81,
            "ShardValue": "11305240000"
          },
          {
            "ShardKey": 82,
            "ShardValue": "11305250000"
          },
          {
            "ShardKey": 83,
            "ShardValue": "11305260000"
          },
          {
            "ShardKey": 84,
            "ShardValue": "11305270000"
          },
          {
            "ShardKey": 85,
            "ShardValue": "11305280000"
          },
          {
            "ShardKey": 86,
            "ShardValue": "11305290000"
          },
          {
            "ShardKey": 87,
            "ShardValue": "11305300000"
          },
          {
            "ShardKey": 88,
            "ShardValue": "11305310000"
          },
          {
            "ShardKey": 89,
            "ShardValue": "11305320000"
          },
          {
            "ShardKey": 90,
            "ShardValue": "11305330000"
          },
          {
            "ShardKey": 91,
            "ShardValue": "11305340000"
          },
          {
            "ShardKey": 92,
            "ShardValue": "11305350000"
          },
          {
            "ShardKey": 93,
            "ShardValue": "11305810000"
          },
          {
            "ShardKey": 94,
            "ShardValue": "11305820000"
          },
          {
            "ShardKey": 95,
            "ShardValue": "11305900000"
          },
          {
            "ShardKey": 96,
            "ShardValue": "11305950000"
          },
          {
            "ShardKey": 97,
            "ShardValue": "11306020000"
          },
          {
            "ShardKey": 98,
            "ShardValue": "11306040000"
          },
          {
            "ShardKey": 99,
            "ShardValue": "11306210000"
          },
          {
            "ShardKey": 100,
            "ShardValue": "11306220000"
          },
          {
            "ShardKey": 101,
            "ShardValue": "11306230000"
          },
          {
            "ShardKey": 102,
            "ShardValue": "11306240000"
          },
          {
            "ShardKey": 103,
            "ShardValue": "11306250000"
          },
          {
            "ShardKey": 104,
            "ShardValue": "11306260000"
          },
          {
            "ShardKey": 105,
            "ShardValue": "11306270000"
          },
          {
            "ShardKey": 106,
            "ShardValue": "11306280000"
          },
          {
            "ShardKey": 107,
            "ShardValue": "11306290000"
          },
          {
            "ShardKey": 108,
            "ShardValue": "11306300000"
          },
          {
            "ShardKey": 109,
            "ShardValue": "11306310000"
          },
          {
            "ShardKey": 110,
            "ShardValue": "11306320000"
          },
          {
            "ShardKey": 111,
            "ShardValue": "11306330000"
          },
          {
            "ShardKey": 112,
            "ShardValue": "11306340000"
          },
          {
            "ShardKey": 113,
            "ShardValue": "11306350000"
          },
          {
            "ShardKey": 114,
            "ShardValue": "11306360000"
          },
          {
            "ShardKey": 115,
            "ShardValue": "11306370000"
          },
          {
            "ShardKey": 116,
            "ShardValue": "11306380000"
          },
          {
            "ShardKey": 117,
            "ShardValue": "11306810000"
          },
          {
            "ShardKey": 118,
            "ShardValue": "11306820000"
          },
          {
            "ShardKey": 119,
            "ShardValue": "11306830000"
          },
          {
            "ShardKey": 120,
            "ShardValue": "11306840000"
          },
          {
            "ShardKey": 121,
            "ShardValue": "11306910000"
          },
          {
            "ShardKey": 122,
            "ShardValue": "11306930000"
          },
          {
            "ShardKey": 123,
            "ShardValue": "11307020000"
          },
          {
            "ShardKey": 124,
            "ShardValue": "11307030000"
          },
          {
            "ShardKey": 125,
            "ShardValue": "11307050000"
          },
          {
            "ShardKey": 126,
            "ShardValue": "11307060000"
          },
          {
            "ShardKey": 127,
            "ShardValue": "11307220000"
          },
          {
            "ShardKey": 128,
            "ShardValue": "11307230000"
          },
          {
            "ShardKey": 129,
            "ShardValue": "11307240000"
          },
          {
            "ShardKey": 130,
            "ShardValue": "11307250000"
          },
          {
            "ShardKey": 131,
            "ShardValue": "11307260000"
          },
          {
            "ShardKey": 132,
            "ShardValue": "11307270000"
          },
          {
            "ShardKey": 133,
            "ShardValue": "11307280000"
          },
          {
            "ShardKey": 134,
            "ShardValue": "11307290000"
          },
          {
            "ShardKey": 135,
            "ShardValue": "11307300000"
          },
          {
            "ShardKey": 136,
            "ShardValue": "11307310000"
          },
          {
            "ShardKey": 137,
            "ShardValue": "11307320000"
          },
          {
            "ShardKey": 138,
            "ShardValue": "11307330000"
          },
          {
            "ShardKey": 139,
            "ShardValue": "11307900000"
          },
          {
            "ShardKey": 140,
            "ShardValue": "11307910000"
          },
          {
            "ShardKey": 141,
            "ShardValue": "11307930000"
          },
          {
            "ShardKey": 142,
            "ShardValue": "11308020000"
          },
          {
            "ShardKey": 143,
            "ShardValue": "11308030000"
          },
          {
            "ShardKey": 144,
            "ShardValue": "11308040000"
          },
          {
            "ShardKey": 145,
            "ShardValue": "11308210000"
          },
          {
            "ShardKey": 146,
            "ShardValue": "11308220000"
          },
          {
            "ShardKey": 147,
            "ShardValue": "11308230000"
          },
          {
            "ShardKey": 148,
            "ShardValue": "11308240000"
          },
          {
            "ShardKey": 149,
            "ShardValue": "11308250000"
          },
          {
            "ShardKey": 150,
            "ShardValue": "11308260000"
          },
          {
            "ShardKey": 151,
            "ShardValue": "11308270000"
          },
          {
            "ShardKey": 152,
            "ShardValue": "11308280000"
          },
          {
            "ShardKey": 153,
            "ShardValue": "11308900000"
          },
          {
            "ShardKey": 154,
            "ShardValue": "11308910000"
          },
          {
            "ShardKey": 155,
            "ShardValue": "11309020000"
          },
          {
            "ShardKey": 156,
            "ShardValue": "11309030000"
          },
          {
            "ShardKey": 157,
            "ShardValue": "11309210000"
          },
          {
            "ShardKey": 158,
            "ShardValue": "11309220000"
          },
          {
            "ShardKey": 159,
            "ShardValue": "11309230000"
          },
          {
            "ShardKey": 160,
            "ShardValue": "11309240000"
          },
          {
            "ShardKey": 161,
            "ShardValue": "11309250000"
          },
          {
            "ShardKey": 162,
            "ShardValue": "11309260000"
          },
          {
            "ShardKey": 163,
            "ShardValue": "11309270000"
          },
          {
            "ShardKey": 164,
            "ShardValue": "11309280000"
          },
          {
            "ShardKey": 165,
            "ShardValue": "11309290000"
          },
          {
            "ShardKey": 166,
            "ShardValue": "11309300000"
          },
          {
            "ShardKey": 167,
            "ShardValue": "11309810000"
          },
          {
            "ShardKey": 168,
            "ShardValue": "11309820000"
          },
          {
            "ShardKey": 169,
            "ShardValue": "11309830000"
          },
          {
            "ShardKey": 170,
            "ShardValue": "11309840000"
          },
          {
            "ShardKey": 171,
            "ShardValue": "11309900000"
          },
          {
            "ShardKey": 172,
            "ShardValue": "11309910000"
          },
          {
            "ShardKey": 173,
            "ShardValue": "11309920000"
          },
          {
            "ShardKey": 174,
            "ShardValue": "11309930000"
          },
          {
            "ShardKey": 175,
            "ShardValue": "11309940000"
          },
          {
            "ShardKey": 176,
            "ShardValue": "11310020000"
          },
          {
            "ShardKey": 177,
            "ShardValue": "11310030000"
          },
          {
            "ShardKey": 178,
            "ShardValue": "11310220000"
          },
          {
            "ShardKey": 179,
            "ShardValue": "11310230000"
          },
          {
            "ShardKey": 180,
            "ShardValue": "11310240000"
          },
          {
            "ShardKey": 181,
            "ShardValue": "11310250000"
          },
          {
            "ShardKey": 182,
            "ShardValue": "11310260000"
          },
          {
            "ShardKey": 183,
            "ShardValue": "11310280000"
          },
          {
            "ShardKey": 184,
            "ShardValue": "11310810000"
          },
          {
            "ShardKey": 185,
            "ShardValue": "11310820000"
          },
          {
            "ShardKey": 186,
            "ShardValue": "11310900000"
          },
          {
            "ShardKey": 187,
            "ShardValue": "11311020000"
          },
          {
            "ShardKey": 188,
            "ShardValue": "11311210000"
          },
          {
            "ShardKey": 189,
            "ShardValue": "11311220000"
          },
          {
            "ShardKey": 190,
            "ShardValue": "11311230000"
          },
          {
            "ShardKey": 191,
            "ShardValue": "11311240000"
          },
          {
            "ShardKey": 192,
            "ShardValue": "11311250000"
          },
          {
            "ShardKey": 193,
            "ShardValue": "11311260000"
          },
          {
            "ShardKey": 194,
            "ShardValue": "11311270000"
          },
          {
            "ShardKey": 195,
            "ShardValue": "11311280000"
          },
          {
            "ShardKey": 196,
            "ShardValue": "11311810000"
          },
          {
            "ShardKey": 197,
            "ShardValue": "11311820000"
          },
          {
            "ShardKey": 198,
            "ShardValue": "11311900000"
          },
          {
            "ShardKey": 199,
            "ShardValue": "11311910000"
          },
          {
            "ShardKey": 200,
            "ShardValue": "11331010000"
          },
          {
            "ShardKey": 201,
            "ShardValue": "11331020000"
          },
          {
            "ShardKey": 202,
            "ShardValue": "11331030000"
          }
        ],
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "80",
            "GroupId": get_GroupID('scsj-ztzx-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)


# 完税证明转开消息提醒
def tsf_CreateTask_WszmZktxExcuteTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 3600000,
            "TaskName": "完税证明转开消息提醒",
            "TaskContent": "cn.gov.chinatax.gt4.skzs.task.sswszm.WszmZktxExcuteTask",
            "ExecuteType": "shard",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 0 22 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "ShardCount": 202,
            "ShardArguments": [
          {
            "ShardKey": 1,
            "ShardValue": "11301020000"
          },
          {
            "ShardKey": 2,
            "ShardValue": "11301040000"
          },
          {
            "ShardKey": 3,
            "ShardValue": "11301050000"
          },
          {
            "ShardKey": 4,
            "ShardValue": "11301070000"
          },
          {
            "ShardKey": 5,
            "ShardValue": "11301080000"
          },
          {
            "ShardKey": 6,
            "ShardValue": "11301090000"
          },
          {
            "ShardKey": 7,
            "ShardValue": "11301100000"
          },
          {
            "ShardKey": 8,
            "ShardValue": "11301110000"
          },
          {
            "ShardKey": 9,
            "ShardValue": "11301210000"
          },
          {
            "ShardKey": 10,
            "ShardValue": "11301230000"
          },
          {
            "ShardKey": 11,
            "ShardValue": "11301250000"
          },
          {
            "ShardKey": 12,
            "ShardValue": "11301260000"
          },
          {
            "ShardKey": 13,
            "ShardValue": "11301270000"
          },
          {
            "ShardKey": 14,
            "ShardValue": "11301280000"
          },
          {
            "ShardKey": 15,
            "ShardValue": "11301290000"
          },
          {
            "ShardKey": 16,
            "ShardValue": "11301300000"
          },
          {
            "ShardKey": 17,
            "ShardValue": "11301310000"
          },
          {
            "ShardKey": 18,
            "ShardValue": "11301320000"
          },
          {
            "ShardKey": 19,
            "ShardValue": "11301330000"
          },
          {
            "ShardKey": 20,
            "ShardValue": "11301810000"
          },
          {
            "ShardKey": 21,
            "ShardValue": "11301830000"
          },
          {
            "ShardKey": 22,
            "ShardValue": "11301840000"
          },
          {
            "ShardKey": 23,
            "ShardValue": "11301900000"
          },
          {
            "ShardKey": 24,
            "ShardValue": "11301910000"
          },
          {
            "ShardKey": 25,
            "ShardValue": "11301920000"
          },
          {
            "ShardKey": 26,
            "ShardValue": "11301940000"
          },
          {
            "ShardKey": 27,
            "ShardValue": "11302020000"
          },
          {
            "ShardKey": 28,
            "ShardValue": "11302030000"
          },
          {
            "ShardKey": 29,
            "ShardValue": "11302040000"
          },
          {
            "ShardKey": 30,
            "ShardValue": "11302050000"
          },
          {
            "ShardKey": 31,
            "ShardValue": "11302070000"
          },
          {
            "ShardKey": 32,
            "ShardValue": "11302080000"
          },
          {
            "ShardKey": 33,
            "ShardValue": "11302090000"
          },
          {
            "ShardKey": 34,
            "ShardValue": "11302230000"
          },
          {
            "ShardKey": 35,
            "ShardValue": "11302240000"
          },
          {
            "ShardKey": 36,
            "ShardValue": "11302250000"
          },
          {
            "ShardKey": 37,
            "ShardValue": "11302270000"
          },
          {
            "ShardKey": 38,
            "ShardValue": "11302290000"
          },
          {
            "ShardKey": 39,
            "ShardValue": "11302810000"
          },
          {
            "ShardKey": 40,
            "ShardValue": "11302830000"
          },
          {
            "ShardKey": 41,
            "ShardValue": "11302900000"
          },
          {
            "ShardKey": 42,
            "ShardValue": "11302910000"
          },
          {
            "ShardKey": 43,
            "ShardValue": "11302930000"
          },
          {
            "ShardKey": 44,
            "ShardValue": "11302940000"
          },
          {
            "ShardKey": 45,
            "ShardValue": "11302950000"
          },
          {
            "ShardKey": 46,
            "ShardValue": "11302960000"
          },
          {
            "ShardKey": 47,
            "ShardValue": "11303020000"
          },
          {
            "ShardKey": 48,
            "ShardValue": "11303030000"
          },
          {
            "ShardKey": 49,
            "ShardValue": "11303040000"
          },
          {
            "ShardKey": 50,
            "ShardValue": "11303210000"
          },
          {
            "ShardKey": 51,
            "ShardValue": "11303220000"
          },
          {
            "ShardKey": 52,
            "ShardValue": "11303230000"
          },
          {
            "ShardKey": 53,
            "ShardValue": "11303240000"
          },
          {
            "ShardKey": 54,
            "ShardValue": "11303900000"
          },
          {
            "ShardKey": 55,
            "ShardValue": "11303930000"
          },
          {
            "ShardKey": 56,
            "ShardValue": "11304020000"
          },
          {
            "ShardKey": 57,
            "ShardValue": "11304030000"
          },
          {
            "ShardKey": 58,
            "ShardValue": "11304040000"
          },
          {
            "ShardKey": 59,
            "ShardValue": "11304060000"
          },
          {
            "ShardKey": 60,
            "ShardValue": "11304230000"
          },
          {
            "ShardKey": 61,
            "ShardValue": "11304240000"
          },
          {
            "ShardKey": 62,
            "ShardValue": "11304250000"
          },
          {
            "ShardKey": 63,
            "ShardValue": "11304260000"
          },
          {
            "ShardKey": 64,
            "ShardValue": "11304270000"
          },
          {
            "ShardKey": 65,
            "ShardValue": "11304280000"
          },
          {
            "ShardKey": 66,
            "ShardValue": "11304290000"
          },
          {
            "ShardKey": 67,
            "ShardValue": "11304300000"
          },
          {
            "ShardKey": 68,
            "ShardValue": "11304310000"
          },
          {
            "ShardKey": 69,
            "ShardValue": "11304320000"
          },
          {
            "ShardKey": 70,
            "ShardValue": "11304330000"
          },
          {
            "ShardKey": 71,
            "ShardValue": "11304340000"
          },
          {
            "ShardKey": 72,
            "ShardValue": "11304350000"
          },
          {
            "ShardKey": 73,
            "ShardValue": "11304810000"
          },
          {
            "ShardKey": 74,
            "ShardValue": "11304900000"
          },
          {
            "ShardKey": 75,
            "ShardValue": "11304910000"
          },
          {
            "ShardKey": 76,
            "ShardValue": "11305020000"
          },
          {
            "ShardKey": 77,
            "ShardValue": "11305030000"
          },
          {
            "ShardKey": 78,
            "ShardValue": "11305210000"
          },
          {
            "ShardKey": 79,
            "ShardValue": "11305220000"
          },
          {
            "ShardKey": 80,
            "ShardValue": "11305230000"
          },
          {
            "ShardKey": 81,
            "ShardValue": "11305240000"
          },
          {
            "ShardKey": 82,
            "ShardValue": "11305250000"
          },
          {
            "ShardKey": 83,
            "ShardValue": "11305260000"
          },
          {
            "ShardKey": 84,
            "ShardValue": "11305270000"
          },
          {
            "ShardKey": 85,
            "ShardValue": "11305280000"
          },
          {
            "ShardKey": 86,
            "ShardValue": "11305290000"
          },
          {
            "ShardKey": 87,
            "ShardValue": "11305300000"
          },
          {
            "ShardKey": 88,
            "ShardValue": "11305310000"
          },
          {
            "ShardKey": 89,
            "ShardValue": "11305320000"
          },
          {
            "ShardKey": 90,
            "ShardValue": "11305330000"
          },
          {
            "ShardKey": 91,
            "ShardValue": "11305340000"
          },
          {
            "ShardKey": 92,
            "ShardValue": "11305350000"
          },
          {
            "ShardKey": 93,
            "ShardValue": "11305810000"
          },
          {
            "ShardKey": 94,
            "ShardValue": "11305820000"
          },
          {
            "ShardKey": 95,
            "ShardValue": "11305900000"
          },
          {
            "ShardKey": 96,
            "ShardValue": "11305950000"
          },
          {
            "ShardKey": 97,
            "ShardValue": "11306020000"
          },
          {
            "ShardKey": 98,
            "ShardValue": "11306040000"
          },
          {
            "ShardKey": 99,
            "ShardValue": "11306210000"
          },
          {
            "ShardKey": 100,
            "ShardValue": "11306220000"
          },
          {
            "ShardKey": 101,
            "ShardValue": "11306230000"
          },
          {
            "ShardKey": 102,
            "ShardValue": "11306240000"
          },
          {
            "ShardKey": 103,
            "ShardValue": "11306250000"
          },
          {
            "ShardKey": 104,
            "ShardValue": "11306260000"
          },
          {
            "ShardKey": 105,
            "ShardValue": "11306270000"
          },
          {
            "ShardKey": 106,
            "ShardValue": "11306280000"
          },
          {
            "ShardKey": 107,
            "ShardValue": "11306290000"
          },
          {
            "ShardKey": 108,
            "ShardValue": "11306300000"
          },
          {
            "ShardKey": 109,
            "ShardValue": "11306310000"
          },
          {
            "ShardKey": 110,
            "ShardValue": "11306320000"
          },
          {
            "ShardKey": 111,
            "ShardValue": "11306330000"
          },
          {
            "ShardKey": 112,
            "ShardValue": "11306340000"
          },
          {
            "ShardKey": 113,
            "ShardValue": "11306350000"
          },
          {
            "ShardKey": 114,
            "ShardValue": "11306360000"
          },
          {
            "ShardKey": 115,
            "ShardValue": "11306370000"
          },
          {
            "ShardKey": 116,
            "ShardValue": "11306380000"
          },
          {
            "ShardKey": 117,
            "ShardValue": "11306810000"
          },
          {
            "ShardKey": 118,
            "ShardValue": "11306820000"
          },
          {
            "ShardKey": 119,
            "ShardValue": "11306830000"
          },
          {
            "ShardKey": 120,
            "ShardValue": "11306840000"
          },
          {
            "ShardKey": 121,
            "ShardValue": "11306910000"
          },
          {
            "ShardKey": 122,
            "ShardValue": "11306930000"
          },
          {
            "ShardKey": 123,
            "ShardValue": "11307020000"
          },
          {
            "ShardKey": 124,
            "ShardValue": "11307030000"
          },
          {
            "ShardKey": 125,
            "ShardValue": "11307050000"
          },
          {
            "ShardKey": 126,
            "ShardValue": "11307060000"
          },
          {
            "ShardKey": 127,
            "ShardValue": "11307220000"
          },
          {
            "ShardKey": 128,
            "ShardValue": "11307230000"
          },
          {
            "ShardKey": 129,
            "ShardValue": "11307240000"
          },
          {
            "ShardKey": 130,
            "ShardValue": "11307250000"
          },
          {
            "ShardKey": 131,
            "ShardValue": "11307260000"
          },
          {
            "ShardKey": 132,
            "ShardValue": "11307270000"
          },
          {
            "ShardKey": 133,
            "ShardValue": "11307280000"
          },
          {
            "ShardKey": 134,
            "ShardValue": "11307290000"
          },
          {
            "ShardKey": 135,
            "ShardValue": "11307300000"
          },
          {
            "ShardKey": 136,
            "ShardValue": "11307310000"
          },
          {
            "ShardKey": 137,
            "ShardValue": "11307320000"
          },
          {
            "ShardKey": 138,
            "ShardValue": "11307330000"
          },
          {
            "ShardKey": 139,
            "ShardValue": "11307900000"
          },
          {
            "ShardKey": 140,
            "ShardValue": "11307910000"
          },
          {
            "ShardKey": 141,
            "ShardValue": "11307930000"
          },
          {
            "ShardKey": 142,
            "ShardValue": "11308020000"
          },
          {
            "ShardKey": 143,
            "ShardValue": "11308030000"
          },
          {
            "ShardKey": 144,
            "ShardValue": "11308040000"
          },
          {
            "ShardKey": 145,
            "ShardValue": "11308210000"
          },
          {
            "ShardKey": 146,
            "ShardValue": "11308220000"
          },
          {
            "ShardKey": 147,
            "ShardValue": "11308230000"
          },
          {
            "ShardKey": 148,
            "ShardValue": "11308240000"
          },
          {
            "ShardKey": 149,
            "ShardValue": "11308250000"
          },
          {
            "ShardKey": 150,
            "ShardValue": "11308260000"
          },
          {
            "ShardKey": 151,
            "ShardValue": "11308270000"
          },
          {
            "ShardKey": 152,
            "ShardValue": "11308280000"
          },
          {
            "ShardKey": 153,
            "ShardValue": "11308900000"
          },
          {
            "ShardKey": 154,
            "ShardValue": "11308910000"
          },
          {
            "ShardKey": 155,
            "ShardValue": "11309020000"
          },
          {
            "ShardKey": 156,
            "ShardValue": "11309030000"
          },
          {
            "ShardKey": 157,
            "ShardValue": "11309210000"
          },
          {
            "ShardKey": 158,
            "ShardValue": "11309220000"
          },
          {
            "ShardKey": 159,
            "ShardValue": "11309230000"
          },
          {
            "ShardKey": 160,
            "ShardValue": "11309240000"
          },
          {
            "ShardKey": 161,
            "ShardValue": "11309250000"
          },
          {
            "ShardKey": 162,
            "ShardValue": "11309260000"
          },
          {
            "ShardKey": 163,
            "ShardValue": "11309270000"
          },
          {
            "ShardKey": 164,
            "ShardValue": "11309280000"
          },
          {
            "ShardKey": 165,
            "ShardValue": "11309290000"
          },
          {
            "ShardKey": 166,
            "ShardValue": "11309300000"
          },
          {
            "ShardKey": 167,
            "ShardValue": "11309810000"
          },
          {
            "ShardKey": 168,
            "ShardValue": "11309820000"
          },
          {
            "ShardKey": 169,
            "ShardValue": "11309830000"
          },
          {
            "ShardKey": 170,
            "ShardValue": "11309840000"
          },
          {
            "ShardKey": 171,
            "ShardValue": "11309900000"
          },
          {
            "ShardKey": 172,
            "ShardValue": "11309910000"
          },
          {
            "ShardKey": 173,
            "ShardValue": "11309920000"
          },
          {
            "ShardKey": 174,
            "ShardValue": "11309930000"
          },
          {
            "ShardKey": 175,
            "ShardValue": "11309940000"
          },
          {
            "ShardKey": 176,
            "ShardValue": "11310020000"
          },
          {
            "ShardKey": 177,
            "ShardValue": "11310030000"
          },
          {
            "ShardKey": 178,
            "ShardValue": "11310220000"
          },
          {
            "ShardKey": 179,
            "ShardValue": "11310230000"
          },
          {
            "ShardKey": 180,
            "ShardValue": "11310240000"
          },
          {
            "ShardKey": 181,
            "ShardValue": "11310250000"
          },
          {
            "ShardKey": 182,
            "ShardValue": "11310260000"
          },
          {
            "ShardKey": 183,
            "ShardValue": "11310280000"
          },
          {
            "ShardKey": 184,
            "ShardValue": "11310810000"
          },
          {
            "ShardKey": 185,
            "ShardValue": "11310820000"
          },
          {
            "ShardKey": 186,
            "ShardValue": "11310900000"
          },
          {
            "ShardKey": 187,
            "ShardValue": "11311020000"
          },
          {
            "ShardKey": 188,
            "ShardValue": "11311210000"
          },
          {
            "ShardKey": 189,
            "ShardValue": "11311220000"
          },
          {
            "ShardKey": 190,
            "ShardValue": "11311230000"
          },
          {
            "ShardKey": 191,
            "ShardValue": "11311240000"
          },
          {
            "ShardKey": 192,
            "ShardValue": "11311250000"
          },
          {
            "ShardKey": 193,
            "ShardValue": "11311260000"
          },
          {
            "ShardKey": 194,
            "ShardValue": "11311270000"
          },
          {
            "ShardKey": 195,
            "ShardValue": "11311280000"
          },
          {
            "ShardKey": 196,
            "ShardValue": "11311810000"
          },
          {
            "ShardKey": 197,
            "ShardValue": "11311820000"
          },
          {
            "ShardKey": 198,
            "ShardValue": "11311900000"
          },
          {
            "ShardKey": 199,
            "ShardValue": "11311910000"
          },
          {
            "ShardKey": 200,
            "ShardValue": "11331010000"
          },
          {
            "ShardKey": 201,
            "ShardValue": "11331020000"
          },
          {
            "ShardKey": 202,
            "ShardValue": "11331030000"
          }
        ],
            "AdvanceSettings": {
                "SubTaskConcurrency": 3
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "TaskArgument": "skssqq=2014-01-01;skssqz=2099-01-01",
            "GroupId": get_GroupID('scsj-skzs-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)


# 扫描预约定时扣款
def tsf_CreateTask_YykkExecuteTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 36000000,
            "TaskName": "扫描预约定时扣款",
            "TaskContent": "cn.gov.chinatax.gt4.skzs.task.yjkp.YykkExecuteTask",
            "ExecuteType": "shard",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 0 2,12,18 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "ShardCount": 244,
            "AdvanceSettings": {
                "SubTaskConcurrency": 1
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "90",
            "GroupId": get_GroupID('scsj-skzs-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)

# 同步网上领票审核结果
def tsf_CreateTask_WslpzttbTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 60000,
            "TaskName": "同步网上领票审核结果",
            "TaskContent": "cn.gov.chinatax.gt4.ztxxbg.task.wslpzttb.WslpzttbTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 55 0/6 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-ztxxbg-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)

# 随机抽查自查_复核通过监控
def tsf_CreateTask_QueryFhtgYjsfTaskk():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 60000,
            "TaskName": "随机抽查自查_复核通过监控",
            "TaskContent": "cn.gov.chinatax.gt4.jcaj.task.QueryFhtgYjsfTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 0 5 ? * *"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-ztxxbg-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)

# 同步金三工作流审批结果
def tsf_CreateTask_SxzttbTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 300000,
            "TaskName": "同步金三工作流审批结果",
            "TaskContent": "cn.gov.chinatax.gt4.sqsp.task.sxzttb.SxzttbTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 40 0/6 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-sqsp-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)

# 合并分立报告_企业未在规定时间内进行对应业务办理的监控
def tsf_CreateTask_HbflbgTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 60000,
            "TaskName": "合并分立报告_企业未在规定时间内进行对应业务办理的监控",
            "TaskContent": "cn.gov.chinatax.gt4.ztxxbg.task.hbflbg.HbflbgTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 0 0 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-ztxxbg-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)

# 企业所得税清算报备定时将超期数据发起调查巡查
def tsf_CreateTask_QysdsqsbbTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 60000,
            "TaskName": "企业所得税清算报备定时将超期数据发起调查巡查",
            "TaskContent": "cn.gov.chinatax.gt4.ztxxbg.task.qysdsqsbb.QysdsqsbbTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 0 0 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-ztxxbg-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)


# 网上领票同步金三状态
def tsf_CreateTask_WslpzttbTask():
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.CreateTaskRequest()
        params = {
            "TimeOut": 60000,
            "TaskName": "网上领票同步金三状态",
            "TaskContent": "cn.gov.chinatax.gt4.ztxxbg.task.wslpzttb.WslpzttbTask",
            "ExecuteType": "unicast",
            "TaskType": "java",
            "TaskRule": {
              "RuleType": "Cron",
              "Expression": "0 55 0/6 * * ?"
            },
            "RetryCount": 0,
            "RetryInterval": 0,
            "AdvanceSettings": {
                "SubTaskConcurrency": 2
            },
            "SuccessOperator": "GTE",
            "SuccessRatio": "100",
            "GroupId": get_GroupID('scsj-ztxxbg-service')
        }
        req.from_json_string(json.dumps(params))

        resp = client.CreateTask(req)
        return json.loads(resp.to_json_string())
        #print(resp)

    except TencentCloudSDKException as err:
        print(err)


def tsf_StartContainerGroup(self):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)

        req = models.StartContainerGroupRequest()
        params = {
            "GroupId": self
        }
        req.from_json_string(json.dumps(params))

        resp = client.StartContainerGroup(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)


def tsf_DeployContainerGroup(self):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = tce_endpoint
        httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
        httpProfile.keepAlive = True  # 状态保持，默认是False
        httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
        httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
        # 跳过证书校验
        httpProfile.certification = False
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tsf_client.TsfClient(cred, tce_region, clientProfile)
        req = models.DeployContainerGroupRequest()
        GroupId=get_GroupID(self)
        params = {
            "GroupId": GroupId,
            "Reponame": "tsf_100004603073/%s" % (self),
            "TagName": "v1",
            "CpuLimit": "2",
            "MemLimit": "8192",
            "InstanceNum": 1,
            "JvmOpts": "-Xms4g -Xmx6g -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=512m -Dspring.profiles.active=tsf",
            "CpuRequest": "2",
            "MemRequest": "8192",
            "DoNotStart": True,
            "RepoName": "tsf_100004603073/%s" % (self),
            "UpdateType": 0,
            "UpdateIvl": 10,
            "AgentCpuRequest": "0.5",
            "AgentCpuLimit": "0.5",
            "AgentMemRequest": "1024",
            "AgentMemLimit": "1024",
            "ServiceSetting": {
                "ProtocolPorts": [
                    {
                        "Protocol": "TCP",
                        "Port": 8080,
                        "TargetPort": 80
                    }
                ],
                "AccessType": 3,
                "SubnetId": "subnet-m0rk1g0u"
            },
            "DeployAgent": True
        }
        req.from_json_string(json.dumps(params))

        resp = client.DeployContainerGroup(req)
        print(resp.to_json_string())
        #tsf_StartContainerGroup(GroupId)

    except TencentCloudSDKException as err:
        print(err)


# tsf_CreateTask_JcsbRetryTask()
# tsf_CreateTask_ZzslddqTask()
# tsf_CreateTask_WszmZktxExcuteTask()
# tsf_CreateTask_YykkExecuteTask()
# tsf_CreateTask_WslpzttbTask()
# tsf_CreateTask_QueryFhtgYjsfTaskk()
# tsf_CreateTask_HbflbgTask()
# tsf_CreateTask_QysdsqsbbTask()
# tsf_CreateTask_WslpzttbTask()
# tsf_CreateTask_SxzttbTask()
#tsf_StartContainerGroup('yscsj-cxssb-service')
        
import os
filepath='/data/dada/da/dd/config.yaml'
print(os.path.basename(filepath))