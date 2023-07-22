import json,os
from configparser import ConfigParser
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tsf.v20180326 import tsf_client, models

try:
    config = ConfigParser() 
    # 配置文件带中文字符，必须定义编码方式
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

except Exception as err:
    print('配置文件解析失败，请确认\n',err)
    exit(-1)

# 创建微服务应用
def tsf_CreateApplication(self):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        cred = credential.Credential(secret_id, secret_key)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = tsf_endpoint
        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
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

# 获取最新的配置文件  
# 接口名称 ：DescribeConfigs
# todo list
'''
requests 
{
  "action": "DescribeConfigs",
  "serviceType": "tsf",
  "regionId": 1,
  "data": {
    "Version": "2018-03-26",
    "ConfigName": "yscsj-dksq-service",
    "ApplicationId": "application-a2bq5bwa",
    "OrderBy": "creation_time",
    "OrderType": 1,
    "Limit": 20,
    "Offset": 0
  },
  "cmd": "DescribeConfigs"
}
'''


# 获取最新的镜像版本号
# DescribeContainerGroups

'''
{
	"Response": {
		"RequestId": "41a08459-9e0b-4609-841b-0859d6f844e1",
		"Result": {
			"Content": [
				{
					"ClusterId": "cls-xxxxxxx",
					"ClusterName": "示例",
					"CpuLimit": "2.00",
					"CpuRequest": "",
					"CreateTime": "",
					"GroupId": "group-xxxxxxx",
					"GroupName": "test",
					"MemLimit": "4096.00",
					"MemRequest": "",
					"NamespaceId": "namespace-xxxxxxx",
					"NamespaceName": "test",
					"Reponame": "tsf_410xxxxxxx/test",
					"Server": "ccr.ccs.tencentyun.com",
					"TagName": "20190517xxxxxxx"
				}
			],
			"TotalCount": 1
		}
	}
}
'''

if __name__=="__main__":
    for i in range(0,len(app_list)):
        print(app_list[i])
        # .strip()处理下字符前后空格
        #print(tsf_CreateApplication(app_list[i]).strip())