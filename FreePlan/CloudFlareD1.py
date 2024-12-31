# -*-coding:utf-8 -*-
import requests,time,os,yaml,sys,json
# Get configurations
def ReadYaml(YamlPath: str, MainNode: str ):
    try:
        with open(YamlPath, 'r', encoding='utf-8') as file:
            config=yaml.safe_load(file)
        D1_url=config[MainNode]['D1_url']
        Authorization=config[MainNode]['Authorization']
        Auth_Key=config[MainNode]['X-Auth-Key']
        Auth_Email=config[MainNode]['X-Auth-Email']
        return D1_url,Authorization,Auth_Key,Auth_Email
    except Exception as err:
        print('resolve file error. please check!', err)
        sys.exit(1)

# D1 Database Request
class D1SdkClient():
    r"""
    :init D1_url, Authorization,Auth_Key,Auth_Email
    """
    def __init__(self,D1_url,Authorization,Auth_Key,Auth_Email):
        self.D1_url=D1_url
        self.Authorization=Authorization
        self.Auth_Key=Auth_Key
        self.Auth_Email=Auth_Email

    def InsertPayload(self,sys_code,event_type,event_name,remark,event_url=None,img_path=None):
        event_url=event_url if event_url else ""
        img_path=img_path if img_path else ""
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        payload={
            "params": [sys_code,event_type,timestamp,event_name,remark,event_url,img_path],
            "sql": '''INSERT INTO gt4_info (sys_code, event_type,timestamp, event_name,remark,event_url,img_path) VALUES (?,?,?,?,?,?,?);'''
        }
        return payload

    def SelectPayload(self,key,value,column=None,table=None):
        table=table if table else "gt4_info"
        column=column if column else "*"
        payload={
            "params": [],
            "sql": f'''SELECT {column} FROM {table} WHERE {key}="{value}";'''
        }
        return payload
     
    # Create D1 Client
    def QueryD1Client(self,payload):
        headers={
            "Content-Type": "application/json",
            "X-Auth-Email": self.Auth_Email,
            "Authorization": self.Authorization,
            "X-Auth-Key": self.Auth_Key
        }
        response = requests.post(self.D1_url, json=payload, headers=headers)
        return response.text

    # Create D1 Query
    # def InsertD1Query(self,sys_code,event_type,event_name,remark,event_url=None,img_path=None):
    #     event_url=event_url if event_url else ""
    #     img_path=img_path if img_path else ""
    #     headers={
    #         "Content-Type": "application/json",
    #         "X-Auth-Email": self.Auth_Email,
    #         "Authorization": self.Authorization,
    #         "X-Auth-Key": self.Auth_Key
    #     }
    #     timestamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    #     #timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    #     payload={
    #         "params": [sys_code,event_type,timestamp,event_name,remark,event_url,img_path],
    #         "sql": '''INSERT INTO gt4_info (sys_code, event_type,timestamp, event_name,remark,event_url,img_path) VALUES (?,?,?,?,?,?,?);'''
    #     }
    #     #response = requests.request("POST", self.D1_url, json=payload, headers=headers)
    #     response = requests.post(self.D1_url, json=payload, headers=headers)
    #     return response.text

if __name__=="__main__":
    D1_url,Authorization,Auth_Key,Auth_Email=ReadYaml("./CloudFlareD1Config.yaml","D1")
    S3StorageRequest=D1SdkClient(D1_url,Authorization,Auth_Key,Auth_Email)
    PayLoad=S3StorageRequest.InsertPayload("dppt","error","蓝票开具异常","蓝票开具接口请求超时","/kpfw/spHandler?cdlj=blue-invoice-makeout","https://devdoc.eu.org/images/changsha.jpg")
    #PayLoad=S3StorageRequest.SelectPayload("sys_code","xdzswj")
    res=S3StorageRequest.QueryD1Client(payload=PayLoad)
    if json.loads(res)["success"]:
        print(json.loads(res)["result"][0]["results"])
    else:
        print("请求失败:\n",json.loads(res)["messages"])



# payload={
#     "params": [],
#     "sql": """CREATE TABLE `gt4_info` (
#   `sys_code` varchar(18) NOT NULL,
#   `event_type` varchar(18) NOT NULL,
#   `timestamp` datetime ,
#   `event_name` varchar(20) NOT NULL,
#   `remark` varchar(200),
#   `event_url` varchar(200) ,
#   `img_path` varchar(200));"""
# }
