# -*-coding:utf-8 -*-
import requests,yaml
# Get configurations
def ReadYaml(YamlPath: str, MainNode: str ):
    try:
        with open(YamlPath, 'r', encoding='utf-8') as file:
            config=yaml.safe_load(file)
        AI_url=config[MainNode]['AI_url']
        Authorization=config[MainNode]['Authorization']
        Auth_Key=config[MainNode]['X-Auth-Key']
        Auth_Email=config[MainNode]['X-Auth-Email']
        return AI_url,Authorization,Auth_Key,Auth_Email
    except FileNotFoundError as err:
        print(f'File not found: {YamlPath}', err)
        return False
    except yaml.YAMLError as err:
        print('YAML syntax error:', err)
        return False
    except Exception as err:
        print('Unexpected error:', err)
        return False

# CloudFlare AI Request
class AISdkClient():
    r"""
    :init AI_url, Authorization, Auth_Key, Auth_Email
    """
    def __init__(self,AI_url,Authorization,Auth_Key,Auth_Email):
        self.AI_url=AI_url
        self.Authorization=Authorization
        self.Auth_Key=Auth_Key
        self.Auth_Email=Auth_Email

    def GetAIResponse(self,prompt):
        payload = { 
            "role": "user", 
            "prompt": prompt
            }
        headers={
            "Content-Type": "application/json",
            "X-Auth-Email": self.Auth_Email,
            "Authorization": self.Authorization,
            "X-Auth-Key": self.Auth_Key
        }
        response = requests.post(self.AI_url, json=payload, headers=headers).json()
        if response["success"] is True:
            return response["result"]["response"]
        else:
            return response["errors"][0]

if __name__=="__main__":
    AI_url,Authorization,Auth_Key,Auth_Email=ReadYaml("./CloudFlareConfig.yaml","AI")
    AISdkClientRequests=AISdkClient(AI_url,Authorization,Auth_Key,Auth_Email)
    print(AISdkClientRequests.GetAIResponse("""滕王阁序的全篇内容是什么？"""))
