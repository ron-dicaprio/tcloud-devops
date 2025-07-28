import base64,hmac,time,uuid,requests,sys,fastapi,re,uvicorn,os
from urllib import parse

class PyQuickBiSdk():
    def __init__(self,ACCESS_KEY,SECRET_KEY,HOST,Method_URI,HTTP_METHOD,content_type=None):
        self.ACCESS_KEY = ACCESS_KEY
        self.SECRET_KEY = SECRET_KEY
        self.HOST = HOST
        self.Method_URI = Method_URI
        self.HTTP_METHOD = HTTP_METHOD
        self.content_type = content_type or "application/json;charset-utf-8"

    # Base64编码下HMAC-SHA1计算值
    def hash_hmac(self, key, code, algorithm='sha256'):
        hmac_code = hmac.new(key.encode('UTF-8'), code.encode('UTF-8'), algorithm).digest()
        return base64.b64encode(hmac_code).decode()

    # 构造签名
    def Signature(self, UUID, timestamp, Params):
        # Request参数拼接
        # Params主要是用于表单
        if not bool(Params):
            Request_QueryString = ''
        else:
            list = sorted(Params)
            Request_QueryString = '\n'
            for i in list:
                if bool(Params[i]):
                    Request_QueryString = Request_QueryString + i + "=" + str(Params[i]) + "&"
        Request_QueryString = Request_QueryString.strip('&')
        # Requst的Header拼接
        Request_Headers = '\nX-Gw-AccessId:' + self.ACCESS_KEY + '\nX-Gw-Nonce:' + str(UUID) + '\nX-Gw-Timestamp:' + str(timestamp)
        # 待签名字符串
        StringToSign = self.HTTP_METHOD.upper() + '\n' + self.Method_URI + Request_QueryString + Request_Headers
        #print("StringToSign签名字符串:",StringToSign)
        encodeString = parse.quote(StringToSign, '')
        #print("Encode后的签名字符串:", encodeString)
        sign = self.hash_hmac(self.SECRET_KEY, encodeString)
        return sign

    # 请求体
    def get_response(self, jsonParam = None, Params = None):
        jsonParam = jsonParam or {}
        timestamp = str(round(time.time() * 1000))
        UUID_STR = str(uuid.uuid4())
        sign = self.Signature(UUID_STR, timestamp,Params)
        headers = {'X-Gw-AccessId': self.ACCESS_KEY,
           'X-Gw-Nonce': UUID_STR,
           'X-Gw-Timestamp': timestamp,
           'X-Gw-Signature': sign,
           # 开启调试
           'X-Gw-Debug': "false",
           'Content-Type': self.content_type
           }
        try:
            # 后续调整 异步网络请求
            if self.HTTP_METHOD.upper() == "GET":
                resp= requests.get(self.HOST+self.Method_URI, headers=headers,params=Params).json()
            else:
                # 暂时只用到GET请求
                print("Unsupport HTTP Method")
                sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        return resp
    
ACCESS_KEY = "<My QuickBi ACCESS_KEY>"
SECRET_KEY = "<My QuickBi SECRET_KEY>"
HOST = "https://qbi.com"
HTTP_METHOD = "GET"
#userId_pattern = r"^[a-z0-9]{32}$"
userId_REGEX = re.compile(r"^[a-z0-9]{32}$")
# 初始化API实例对象
app=fastapi.FastAPI()
@app.get(path="/api/userId/{userId}")
async def GetBasicInfo(userId:str):
    #if re.match(userId_pattern, userId):
    if userId_REGEX.match(userId):
        Method_URI = f"/openapi/v2/organization/user/{userId}"
        try:
            PyQuickBiSdkRequests = PyQuickBiSdk(ACCESS_KEY, SECRET_KEY, HOST, Method_URI, HTTP_METHOD)
            QbiResp = PyQuickBiSdkRequests.get_response()
            resp={"userId":userId,"nickName":QbiResp["data"]["nickName"]}
            return resp
        except Exception as Err:
            return {"info":"Error","data":Err}
    else:
        return {"info":"Error","data":"userId Formate Error"}

uuId_REGEX = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
@app.get(path="/api/datasetId/{datasetId}")
async def GetdatasetInfo(datasetId:str):
    if uuId_REGEX.match(datasetId):
        Params = {"datasetId": f"{datasetId}"}
        Method_URI = f"/openapi/v2/dataset/infoNew"
        try:
            PyQuickBiSdkRequests = PyQuickBiSdk(ACCESS_KEY, SECRET_KEY, HOST, Method_URI, HTTP_METHOD)
            QbiResp = PyQuickBiSdkRequests.get_response(Params=Params)
            return QbiResp
        except Exception as Err:
            return {"info":"Error","data":Err}
    else:
        return {"info":"Error","data":"datasetId Formate Error"}

@app.get(path="/api/worksId/{worksId}")
async def GetworksId(worksId:str):
    if uuId_REGEX.match(worksId):
        Params = {"worksId": f"{worksId}"}
        Method_URI = f"/openapi/v2/works/query"
        try:
            PyQuickBiSdkRequests = PyQuickBiSdk(ACCESS_KEY, SECRET_KEY, HOST, Method_URI, HTTP_METHOD)
            QbiResp = PyQuickBiSdkRequests.get_response(Params=Params)
            return QbiResp
        except Exception as Err:
            return {"info":"Error","data":Err}
    else:
        return {"info":"Error","data":"datasetId Formate Error"}
    
if __name__ == "__main__":
    # limit workers num ，max to 8
    workers_num=os.cpu_count() if os.cpu_count() < 8 else 8
    uvicorn.run("PyQuickBIApi:app", host="0.0.0.0",port=58080, workers=workers_num, loop="uvloop", http="httptools",reload=False)
    
