# -*- coding: utf-8 -*-
#!/usr/bin/python3
import json,sys,urllib3,time
from tcecloud.common import credential
from tcecloud.common.profile.client_profile import ClientProfile
from tcecloud.common.profile.http_profile import HttpProfile
from tcecloud.monitor.v20180724 import monitor_client, models
# disable_warnings from tcecloud sdk
urllib3.disable_warnings()
tce_client=None
tdsql_instance_list={"tdsqlshard-nzvyqvnz":"电子发票平台_新海关库","tdsqlshard-cdm29ozv":"电子发票平台_机动车库","tdsqlshard-c1til7ph":"电子发票平台_红字通知库","tdsqlshard-ljn14mx9":"电子发票平台_入账库","tdsqlshard-itdvtrmx":"电票生产-发票交付机制-消息库","tdsqlshard-rovfkygf":"电票生产__发票用票库","tdsqlshard-fun25r1h":"电票生产-公共库","tdsqlshard-pq8oqn9d":"电票生产-成品油库","tdsqlshard-133jnjmt":"电子发票纳税人基础信息","tdsqlshard-pjck1qjv":"电子发票管理库","tdsqlshard-lgelsia5":"发票缓存库"}
class TSFSdkClient():
    def __init__(self,tce_region,tce_endpoint,SecretId,SecretKey):
        self.tce_region=tce_region
        self.tce_endpoint=tce_endpoint
        self.SecretId=SecretId
        self.SecretKey=SecretKey

    def tce_CreateClient(self):
        """
        : 初始化httpProfile
        : 创建 tce_client.
        """
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            cred = credential.Credential(self.SecretId, self.SecretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.protocol = "https"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
            httpProfile.keepAlive = True  # 状态保持，多路复用，默认是False
            httpProfile.reqMethod = "POST"  # get请求(默认为post请求)
            httpProfile.reqTimeout = 60    # 请求超时时间，单位为秒(默认60秒)
            # 跳过证书校验
            httpProfile.certification = False
            httpProfile.endpoint = self.tce_endpoint
            # 实例化一个client选项，可选的，没有特殊需求可以跳过
            clientProfile = ClientProfile()
            clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
            clientProfile.language = "en-US"  # 指定展示英文（默认为中文）
            clientProfile.httpProfile = httpProfile
            client = monitor_client.MonitorClient(cred, self.tce_region, clientProfile)
            return client
        except Exception as err:
            print(err)
            sys.exit(-1)

    def monitor_GetMonitorCpuUsageRate(self,StartTime=None,EndTime=None):
        # 判断入参是否正常解析时间类型
        # 前8小时
        StartTime=time.strptime(StartTime, '%Y-%m-%d %H:%M:%S') if StartTime else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()-(8 * 3600)))
        # 当前时间
        EndTime=time.strptime(EndTime, '%Y-%m-%d %H:%M:%S') if EndTime else time.strftime('%Y-%m-%d %H:%M:%S')
        MetricName="CpuUsageRate"
        Namespace="QCE/TDMYSQL" 
        global tce_client
        if not tce_client:
            client=self.tce_CreateClient()
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GetMonitorDataRequest()
            params = {
                "StartTime": StartTime,
                "EndTime": EndTime,
                "Period": 300,
                "Namespace": Namespace,
                "MetricName": MetricName,
                "Instances": [{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-nzvyqvnz"}]} ,{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-cdm29ozv"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-c1til7ph"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-ljn14mx9"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-itdvtrmx"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-rovfkygf"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-fun25r1h"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-pq8oqn9d"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-133jnjmt"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-pjck1qjv"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-lgelsia5"}]}],
            }
            req.from_json_string(json.dumps(params))
            # 输出json格式的字符串回包
            resp = client.GetMonitorData(req).to_json_string()
            Instance_info=[]
            resp_json=json.loads(resp)
            for i in range (0,len(resp_json["DataPoints"])):
                Instance_Id=resp_json['DataPoints'][i]['Dimensions'][0]['Value']
                Instance_Name=tdsql_instance_list[Instance_Id]
                Instance_info.append(f"近8小时{Instance_Name}:{Instance_Id}最大主节点CPU利用率:"+str(max(resp_json["DataPoints"][i]["Values"]))+"%")
            return Instance_info
        except Exception as err:
            return err

    def monitor_GetMonitorLongQuery(self,StartTime=None,EndTime=None):
        # 判断入参是否正常解析时间类型
        # 前8小时
        StartTime=time.strptime(StartTime, '%Y-%m-%d %H:%M:%S') if StartTime else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()-(8 * 3600)))
        # 当前时间
        EndTime=time.strptime(EndTime, '%Y-%m-%d %H:%M:%S') if EndTime else time.strftime('%Y-%m-%d %H:%M:%S')
        MetricName="LongQueryCount"
        Namespace="QCE/TDMYSQL" 
        global tce_client
        if not tce_client:
            client=self.tce_CreateClient()
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GetMonitorDataRequest()
            params = {
                "StartTime": StartTime,
                "EndTime": EndTime,
                "Period": 300,
                "Namespace": Namespace,
                "MetricName": MetricName,
                "Instances": [{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-nzvyqvnz"}]} ,{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-cdm29ozv"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-c1til7ph"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-ljn14mx9"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-itdvtrmx"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-rovfkygf"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-fun25r1h"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-pq8oqn9d"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-133jnjmt"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-pjck1qjv"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-lgelsia5"}]}],
            }
            req.from_json_string(json.dumps(params))
            # 输出json格式的字符串回包
            resp = client.GetMonitorData(req).to_json_string()
            Instance_info=[]
            resp_json=json.loads(resp)
            for i in range (0,len(resp_json["DataPoints"])):
                Instance_Id=resp_json['DataPoints'][i]['Dimensions'][0]['Value']
                Instance_Name=tdsql_instance_list[Instance_Id]
                Instance_info.append(f"近8小时{Instance_Name}:{Instance_Id}汇总主节点慢查询数:"+str(max(resp_json["DataPoints"][i]["Values"]))+"次")
            return Instance_info
        except Exception as err:
            return err

    def monitor_GetMonitorDiskUsedRate(self,StartTime=None,EndTime=None):
        # 判断入参是否正常解析时间类型
        # 前8小时
        StartTime=time.strptime(StartTime, '%Y-%m-%d %H:%M:%S') if StartTime else time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()-(8 * 3600)))
        # 当前时间
        EndTime=time.strptime(EndTime, '%Y-%m-%d %H:%M:%S') if EndTime else time.strftime('%Y-%m-%d %H:%M:%S')
        MetricName="DataDiskUsedRate"
        Namespace="QCE/TDMYSQL" 
        global tce_client
        if not tce_client:
            client=self.tce_CreateClient()
        try:
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.GetMonitorDataRequest()
            params = {
                "StartTime": StartTime,
                "EndTime": EndTime,
                "Period": 300,
                "Namespace": Namespace,
                "MetricName": MetricName,
                "Instances": [{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-nzvyqvnz"}]} ,{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-cdm29ozv"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-c1til7ph"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-ljn14mx9"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-itdvtrmx"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-rovfkygf"}]}, {"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-fun25r1h"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-pq8oqn9d"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-133jnjmt"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-pjck1qjv"}]},{"Dimensions":[{"Name":"InstanceId","Value":"tdsqlshard-lgelsia5"}]}],
            }
            req.from_json_string(json.dumps(params))
            # 输出json格式的字符串回包
            resp = client.GetMonitorData(req).to_json_string()
            Instance_info=[]
            resp_json=json.loads(resp)
            for i in range (0,len(resp_json["DataPoints"])):
                Instance_Id=resp_json['DataPoints'][i]['Dimensions'][0]['Value']
                Instance_Name=tdsql_instance_list[Instance_Id]
                Instance_info.append(f"近8小时{Instance_Name}:{Instance_Id}最大主节点数据磁盘空间利用率:"+str(max(resp_json["DataPoints"][i]["Values"]))+"%")
            return Instance_info
        except Exception as err:
            return err

if __name__=="__main__":
    # 生产及预生产都是通过AKSK判定，禁止弄错
    SecretId='AKID******************V1IO'
    SecretKey='wZsr*********************3uRd'
    tce_region='zjebywxc'
    tce_endpoint='monitor.api3.abc.com'
    TSFSdkCientRequest=TSFSdkClient(tce_region,tce_endpoint,SecretId,SecretKey)
    print("--------开始监控生产数据库CPU使用率--------")
    res_CpuUsageRate=TSFSdkCientRequest.monitor_GetMonitorCpuUsageRate()
    for res in res_CpuUsageRate:
        print(res,"\n")
    print("--------开始监控生产数据库慢查询次数--------")
    res_LongQuery=TSFSdkCientRequest.monitor_GetMonitorLongQuery()
    for res in res_LongQuery:
        print(res,"\n")
    print("--------开始监控生产数据库磁盘使用率--------")
    res_DiskUsed=TSFSdkCientRequest.monitor_GetMonitorDiskUsedRate()
    for res in res_DiskUsed:
        print(res,"\n")
