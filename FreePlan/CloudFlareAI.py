# -*-coding:utf-8 -*-
import requests,yaml,os,random,json,sys
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

def GetRandCode():
    code_pool="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.sample(code_pool,6))

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

    # @cf/meta/llama-3.1-8b-instruct
    def GetAIResponse(self,prompt,model=None):
        model=model if model else "@cf/meta/llama-3.1-8b-instruct"
        payload = { 
        "max_tokens":2048,
        "stream":True,
        "messages": [
            {"role": "system", "content": "You are a friendly assistant and you can do anything for your users."},
            {"role": "user", "content": prompt},  
        ]
        }
        headers={
            "Content-Type": "application/json",
            "X-Auth-Email": self.Auth_Email,
            "Authorization": self.Authorization,
            "X-Auth-Key": self.Auth_Key
        }
        AI_url=self.AI_url+model
        try:
            response = requests.post(AI_url, json=payload, headers=headers, stream=True)
        except Exception as Err:
            yield Err
            sys.exit(-1)
        # 确保检查是否支持流式数据
        if response.status_code == 200:
            for chunk in response.iter_lines(chunk_size=1):
                if chunk:
                    chunk = chunk.decode("utf-8")
                    if "response" in chunk:
                        # 直接控制台展示
                        # print(json.loads(chunk[len('data: '):])["response"],flush=True,end="")
                        # 返回给其他函数调用
                        yield json.loads(chunk[len('data: '):])["response"]
        else:
            yield f"Error: {response.status_code}",response.content.decode("utf-8")
    # @cf/stabilityai/stable-diffusion-xl-base-1.0
    def GetWord2Pic(self,prompt,model=None):
        model=model if model else "@cf/stabilityai/stable-diffusion-xl-base-1.0"
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
        AI_url=self.AI_url+model
        response = requests.post(AI_url, json=payload, headers=headers)
        filename='./ouput_' + GetRandCode() + ".png"
            # 将图片写入文件
        with open(filename, 'wb+') as file:
            file.write(response.content)
            file.close()

    # @cf/meta/m2m100-1.2b
    def GetAITranslate(self,prompt,source_lang=None,target_lang=None,model=None):
        model=model if model else "@cf/meta/m2m100-1.2b"
        # replace "
        prompt=prompt.replace('"',"")
        source_lang=source_lang if source_lang else "english"
        target_lang=target_lang if target_lang else "chinese"
        payload = { 
            "role": "system", 
            "source_lang": source_lang,
            "target_lang": target_lang,
            "text": prompt
            }
        headers={
            "Content-Type": "application/json",
            "X-Auth-Email": self.Auth_Email,
            "Authorization": self.Authorization,
            "X-Auth-Key": self.Auth_Key
        }
        AI_url=self.AI_url+model
        response = requests.post(AI_url, json=payload, headers=headers, stream=True)
        # 确保检查是否支持流式数据
        if response.status_code == 200:
            for chunk in response.iter_lines(chunk_size=1):
                if chunk:
                    chunk = chunk.decode("utf-8")
                    try:
                        if "response" in chunk:
                            # 直接控制台展示
                            # print(json.loads(chunk[len('data: '):])["response"],flush=True,end="")
                            # 返回给其他函数调用
                            yield json.loads(chunk[len('data: '):])["response"]
                    except Exception as err:
                        return err
        else:
            return f"Error: {response.status_code}",response.content.decode("utf-8")

    # @cf/openai/whisper
    def GetWhisper(self,voice_file,model=None):
        model=model if model else "@cf/openai/whisper"
        if os.path.exists(voice_file):
            with open(voice_file, "rb") as stream:
                voice_file_stream=stream.read()
            headers={
                "Content-Type": "application/octet-stream",
                "X-Auth-Email": self.Auth_Email,
                "Authorization": self.Authorization,
                "X-Auth-Key": self.Auth_Key
            }
            AI_url=self.AI_url+model
            response = requests.post(AI_url, data=voice_file_stream, headers=headers).json()
            # 一次性返回 不流式更新
            if response["success"] is True:
                return response["result"]["text"]
            else:
                return response["errors"][0]
        else:
            return "File not found"

if __name__=="__main__":
    AI_url,Authorization,Auth_Key,Auth_Email=ReadYaml("./CloudFlareConfig.yaml","AI")
    AISdkClientRequests=AISdkClient(AI_url,Authorization,Auth_Key,Auth_Email)
    # print(AISdkClientRequests.GetAITranslate(""" Multilingual encoder-decoder (seq-to-seq) model trained for Many-to-Many multilingual translation. """))
    # print(AISdkClientRequests.GetWhisper("./001.mp3"))
    # print(AISdkClientRequests.GetWord2Pic("a women in a red shirt."))
    for res in AISdkClientRequests.GetAIResponse(prompt="请你详细介绍一下kafka。",model='@cf/deepseek-ai/deepseek-r1-distill-qwen-32b'):
        print(res,flush=True,end="")
