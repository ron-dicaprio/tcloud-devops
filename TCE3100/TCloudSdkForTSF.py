# -*- coding: utf-8 -*-
#!/usr/bin/python3
import json,sys,urllib3
from tcecloud.common import credential
from tcecloud.common.profile.client_profile import ClientProfile
from tcecloud.common.profile.http_profile import HttpProfile
from tcecloud.common.exception.cloud_sdk_exception import CloudSDKException
from tcecloud.tsf.v20180326 import tsf_client, models
urllib3.disable_warnings()

class TSFSdkClient():
    def __init__(self,tce_region,tce_endpoint,SecretId,SecretKey):
        self.tce_region=tce_region
        self.tce_endpoint=tce_endpoint
        self.SecretId=SecretId
        self.SecretKey=SecretKey

    def tsf_CreateClient(self):
        """
        : 初始化httpProfile
        : 创建 tsf_client 并 return .
        """
        try:
            # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
            cred = credential.Credential(self.SecretId, self.SecretKey)
            # 实例化一个http选项，可选的，没有特殊需求可以跳过
            httpProfile = HttpProfile()
            httpProfile.protocol = "http"  # 在外网互通的网络环境下支持http协议(默认是https协议),建议使用https协议
            httpProfile.keepAlive = True  # 状态保持，默认是False
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
            client = tsf_client.TsfClient(cred, self.tce_region, clientProfile)
            return client
        except Exception as err:
            return err
            
    def tsf_CreateApplication(self,ApplicationName):
        """
        : TSF-应用管理-新建应用
        : 应用类型为容器  "ApplicationType": "C"
        : 此函数用于创建TSF应用
        """
        try:
            client=self.tsf_CreateClient()
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.CreateApplicationRequest()
            params = {
                # 应用名称
                "ApplicationName": ApplicationName,
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
        except Exception as err:
            return err

    def tsf_GetApplicationID(self,SearchWord):
        """
        : 获取应用的applicationID, 此ID不同于部署组ID
        : SearchWord 应用名称
        """
        try:
            client=self.tsf_CreateClient()
            # 实例化一个请求对象,每个接口都会对应一个request对象
            req = models.DescribeApplicationsRequest()
            params = {
                "SearchWord": SearchWord
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
        except Exception as err:
            return err

    def tsf_CreateGroup(self,GroupName):
        """
        : 创建部署组
        : GroupName 应用名称
        """
        try:
            client=self.tsf_CreateClient()
            req = models.CreateGroupRequest()
            ApplicationId=self.tsf_GetApplicationID(GroupName)
            params = {
                "ApplicationId": ApplicationId,
                "GroupName": GroupName,
                "NamespaceId": NamespaceId,
                "ClusterId": ClusterId
            }
            req.from_json_string(json.dumps(params))
            resp = client.CreateGroup(req)
            return resp.to_json_string()
        except Exception as err:
            return err

    def tsf_GetGroupID(self,GroupName):
        """
        : 获取部署组ID
        : GroupName 应用名称
        """
        try:
            client=self.tsf_CreateClient()
            req = models.DescribeSimpleGroupsRequest()
            params = {
                "SearchWord": GroupName
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeSimpleGroups(req)
            return json.loads(resp.to_json_string())['Result']['Content'][0]['GroupId']
        except Exception as err:
            return err

    def tsf_DescribeConfigs(self,GroupName):
        """
        : 获取应用最新配置文件内容
        : GroupName 应用名称
        """
        try:
            client=self.tsf_CreateClient()
            req = models.DescribeConfigsRequest()
            params = {
                "SearchWord": GroupName
            }
            req.from_json_string(json.dumps(params))

            resp = client.DescribeConfigs(req)
            return json.loads(resp.to_json_string())["Result"]["Content"][0]["ConfigValue"]
        except Exception as err:
            return err

    def tsf_DeployContainerGroup(self,GroupName,TagName):
        """
        : 获取应用最新配置文件内容
        : GroupName 应用名称
        : TagName 应用版本号
        """
        try:
            client=self.tsf_CreateClient()
            req = models.DeployContainerGroupRequest()
            GroupId=self.tsf_GetGroupID(GroupName)
            params = {
                "GroupId": GroupId,
                "Reponame": "%s/%s" % (RepoRoot,GroupName),
                "TagName": TagName,
                "CpuLimit": "2",
                "MemLimit": "8192",
                "InstanceNum": 1,
                "JvmOpts": "-Xms4g -Xmx6g -XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=512m -Dspring.profiles.active=tsf",
                "CpuRequest": "2",
                "MemRequest": "8192",
                "DoNotStart": True,
                "RepoName": "%s/%s" % (RepoRoot,GroupName),
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
                    "SubnetId": SubnetId
                },
                "DeployAgent": True
            }
            req.from_json_string(json.dumps(params))

            resp = client.DeployContainerGroup(req)
            return resp.to_json_string()
        except Exception as err:
            return err
    
    def tsf_StopContainerGroup(self,GroupName):
        """
        : 停止部署组
        : GroupName 应用名称
        """
        try:
            client=self.tsf_CreateClient()
            req = models.DescribeConfigsRequest()
            params = {
                "SearchWord": GroupName
            }
            req = models.StopContainerGroupRequest()
            params = {
                "GroupId": self.tsf_GetGroupID(GroupName)
            }
            req.from_json_string(json.dumps(params))

            resp = client.StopContainerGroup(req)
            return resp.to_json_string()
        except Exception as err:
            return err

if __name__=="__main__":
    # 生产及预生产都是通过AKSK判定，禁止弄错
    SecretId='AKIDQbRwVo*********xmGOBdkVx4pFJ1'
    SecretKey='PTAVU7PLv*********i8CrFNBVbR1IE'
    tce_region='zj**ywxc'
    tce_endpoint='tsf.api3.xc11.cloud.*****'
    TSFSdkCientRequest=TSFSdkClient(tce_region,tce_endpoint,SecretId,SecretKey)
    res=TSFSdkCientRequest.tsf_CreateApplication('yscsj-demo-service')
    print(res)
