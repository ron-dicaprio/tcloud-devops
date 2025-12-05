# -*- coding:utf-8 -*-
import hmac,json,requests,sys,time
from hashlib import sha256
# import urllib3
# urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
# 解决SSLV3_ALERT_HANDSHAKE_FAILURE问题
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
class AnyBackupClient():
    def __init__(self,baseUrl,apiUrl,method,AccessKey, SecretKey,params):
        self.baseUrl=baseUrl
        self.apiUrl=apiUrl
        self.method=method
        self.AccessKey=AccessKey
        self.SecretKey=SecretKey
        self.params=params

    def request_sign(self):
        paramsStr = ""
        if self.baseUrl.upper().startswith("HTTPS"):
            baseIp = self.baseUrl[8:]
        elif self.baseUrl.upper().startswith("HTTP"):
            baseIp = self.baseUrl[7:]
        else:
            print(f"Upsupport url {self.baseUrl}, url should start with http(s) .")
            sys.exit(-1)
        prefixStr = self.method + baseIp + self.apiUrl  
        if len(self.params) > 0:
            paramsStr += "&".join("%s=%s" % (item, self.params[item]) for item in sorted(self.params))

        if self.method == "GET":
            paramsStr = "?" + paramsStr

        if self.method == "POST":
            paramsStr = "?" + json.dumps(self.params)


        reqStr = prefixStr + paramsStr
        # 使用HMAC-SHA256算法生成签名
        signature = hmac.new(self.SecretKey.encode('utf-8'), reqStr.encode('utf-8'), digestmod=sha256).hexdigest()
        return signature, paramsStr

    def request(self):
        method = self.method.upper() or "GET"
        url = self.baseUrl + self.apiUrl
        headers = {"Referer": self.baseUrl}
        paramsStr = ""
        try:
            headers["Content-Type"] = "application/json"
            RequestSign, paramsStr = self.request_sign()
            # 构造签名头部信息
            signature = {"AccessKey": self.AccessKey, 'RequestSign': RequestSign}
            headers["signature"] = json.dumps(signature)

            if method == "GET":
                if paramsStr:
                    url = url + paramsStr
                    params = {}
            # 根据不同的HTTP方法发送请求
            if method == 'GET':
                resp = requests.get(url, params=params, headers=headers, verify=False)
            elif method == 'POST':
                resp = requests.post(url, json=self.params, headers=headers, verify=False)
            else:
                print(f"Upsupport method {method}.")
                sys.exit(-1)
            obj = json.loads(resp.text)
            return obj

        except Exception as err:
            print("HTTP请求失败:", str(err))

# todo: 跟GetErrorList合并 动态传参修改Paramas
def GetRunningList(baseUrl, AccessKey, SecretKey,Num=None):
    Num = Num or 5
    # Num = Num if Num else 5
    Error_params = {
        "count": Num,
        "hasRunning": 1,
        "index": 0,
        "status": ''
    }
    apiUrl='/backups/backup_job/instances'
    error_job_method='GET'
    Error_AnyBackupClientRequests=AnyBackupClient(baseUrl, apiUrl, error_job_method, AccessKey, SecretKey, Error_params)
    resp=Error_AnyBackupClientRequests.request()
    if resp['status']=='success':
        for i in range(0,len(resp['responseData']['data'])):
            print('存在以下任务正在运行中:',resp['responseData']['data'][i]['instJobName'])

def GetErrorList(baseUrl, AccessKey, SecretKey,Num=None):
    Num = Num or 5
    Error_params = {
        "count": Num,
        "hasRunning": 0,
        "index": 0,
        "status": 64
    }
    apiUrl='/backups/backup_job/instances'
    error_job_method='GET'
    Error_AnyBackupClientRequests=AnyBackupClient(baseUrl, apiUrl, error_job_method, AccessKey, SecretKey, Error_params)
    resp=Error_AnyBackupClientRequests.request()
    if resp['status']=='success':
        for i in range(0,len(resp['responseData']['data'])):
            print('存在以下任务执行失败:',resp['responseData']['data'][i]['instJobName'])

def GetAnyBackupList(baseUrl,AccessKey,SecretKey,location):
    # /backups/fusion_job_count :: 本地复制任务
    # /dataprotects/fusion_job_count ：： 远程复制任务
    # /logs/warn/job_warn :: 任务执行告警
    local_apiUrl='/backups/fusion_job_count'
    remote_apiUrl='/datasyncs/dashboard'
    fusion_job_method='GET'
    fusion_job_params = {
        "startTime": int(time.time() * 1000 - 86400000)
    }

    local_AnyBackupClientRequests=AnyBackupClient(baseUrl, local_apiUrl, fusion_job_method, AccessKey, SecretKey, fusion_job_params)
    resp=local_AnyBackupClientRequests.request()
    if resp['status'] == 'success':
        print(location,"---- 本地任务-成功:",resp['responseData']['sucess'],"; 本地任务-运行中:",resp['responseData']['runing'],"; 本地任务-失败:",resp['responseData']['fail'])
        if resp['responseData']['fail'] > 0:
            GetErrorList(baseUrl, AccessKey, SecretKey, resp['responseData']['fail'])
        if resp['responseData']['runing'] > 0:
            GetRunningList(baseUrl, AccessKey, SecretKey, resp['responseData']['runing'])   
    else:
        print(location,"接口调用异常")

    remote_AnyBackupClientRequests=AnyBackupClient(baseUrl, remote_apiUrl, fusion_job_method, AccessKey, SecretKey, fusion_job_params)
    resp=remote_AnyBackupClientRequests.request()
    if resp['status'] == 'success':
        print(location,"---- 远程任务-运行中:",resp['responseData']['sync']['runNum'],"; 远程任务-异常:",resp['responseData']['sync']['readyNum']+resp['responseData']['sync']['pauseNum']+resp['responseData']['sync']['abortNum'],"; 远程任务-已停止:",resp['responseData']['sync']['stopedNum'])
        # if resp['responseData']['sync']['runNum'] > 0:
        #     GetErrorList(baseUrl, AccessKey, SecretKey, resp['responseData']['fail'])
    else:
        print(location,"接口调用异常")
    
if __name__ == "__main__":
    # 用yaml替代AKSK_LISTS对象
    AKSK_LISTS={
        "YunDa_AnyBackup": {"baseUrl": "https://10.100.10.107:9600","AccessKey": "2542********************ad3","SecretKey": "2cce1*****************************a6d004"},
        "NingXiang_AnyBackup": {"baseUrl": "https://10.110.10.148:9600","AccessKey": "b629********************0cfe4","SecretKey":"1d3da****************************************0119"},
        "NingXiangSAP_AnyBackup": {"baseUrl": "https://10.110.10.148:9600","AccessKey": "68f76********************367f50","SecretKey":"85f6****************************************6c90"},
        "TongRen_AnyBackup": {"baseUrl": "https://10.120.10.40:9600","AccessKey": "3c25b********************91e3","SecretKey":"d5d4****************************************f9"},
        "QinZhou_AnyBackup": {"baseUrl": "https://10.130.10.30:9600","AccessKey": "73981********************8c7d","SecretKey":"5de8a****************************************3d9d"},
        "KaiYang_AnyBackup": {"baseUrl": "https://10.150.10.148:9600","AccessKey": "cfea********************dc683","SecretKey":"242d****************************************b6e9"},
        "HangYeYun_AnyBackup": {"baseUrl": "https://10.253.2.48:9600","AccessKey": "89e2********************7b93","SecretKey":"84a6****************************************ae5b4"}  
    }
    for location,value in AKSK_LISTS.items():
        baseUrl,AccessKey,SecretKey=value['baseUrl'],value['AccessKey'],value['SecretKey']
        GetAnyBackupList(baseUrl,AccessKey,SecretKey,location)
