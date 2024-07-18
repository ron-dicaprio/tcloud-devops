# -*-coding:utf-8 -*-
import requests,yaml,sys
# Get configurations
# we use MainNode to combine all configs to a config file.
def ReadYaml(YamlPath: str, MainNode: str ):
    try:
        with open(YamlPath, 'r', encoding='utf-8') as file:
            config=yaml.safe_load(file)
        PutKV_url=config[MainNode]['PutKV_url']
        GetKV_url=config[MainNode]['GetKV_url']
        Authorization=config[MainNode]['Authorization']
        Auth_Key=config[MainNode]['X-Auth-Key']
        Auth_Email=config[MainNode]['X-Auth-Email']
        return PutKV_url,GetKV_url,Authorization,Auth_Key,Auth_Email
    except FileNotFoundError as err:
        print(f'File not found: {YamlPath}', err)
        return False
    except yaml.YAMLError as err:
        print('YAML syntax error:', err)
        return False
    except Exception as err:
        print('Unexpected error:', err)
        return False

# KV Database Request
class KVSdkClient():
    r"""
    :init PutKV_url,GetKV_url,Authorization,Auth_Key,Auth_Email
    """
    def __init__(self,PutKV_url,GetKV_url,Authorization,Auth_Key,Auth_Email):
        self.PutKV_url=PutKV_url
        self.GetKV_url=GetKV_url
        self.Authorization=Authorization
        self.Auth_Key=Auth_Key
        self.Auth_Email=Auth_Email

    def PutKVData(self,key,value):
        payload = [
            {
                "key": key,
                "value": value
            }
        ]
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Email": self.Auth_Email,
            "Authorization": self.Authorization,
            "X-Auth-Key": self.Auth_Key
        }
        response = requests.put(self.PutKV_url, json=payload, headers=headers)
        return response.text

    def GetKVData(self,key):
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Email": self.Auth_Email,
            "Authorization": self.Authorization,
            "X-Auth-Key": self.Auth_Key
        }
        response = requests.get(self.GetKV_url+key,headers=headers)
        return response.text

if __name__=="__main__":
    PutKV_url,GetKV_url,Authorization,Auth_Key,Auth_Email=ReadYaml("./CloudFlareConfig.yaml","KV")
    KVSdkClientRequests=KVSdkClient(PutKV_url,GetKV_url,Authorization,Auth_Key,Auth_Email)
    res=KVSdkClientRequests.GetKVData("ztxxbg-service")
    print(res)
