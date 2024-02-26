#-*- coding:utf-8 -*-
from qcloud_cos import CosConfig,CosS3Client
import urllib3,os,yaml,sys
# disable_warnings()移除警告
urllib3.disable_warnings()
class COSSdkClient():
    r""" 
    : Based On tencentcloud-sdk-python 3.0.1064 .
    : This Is A Class For COS .
    """
    def ReadYaml(self, YamlPath, MainNode):
        r"""
        : 利用PyYAML库读取配置文件
		: YamlPath     YAML配置文件的绝对路径 或工作路径对应的文件相对路径
        : MainNode     YAML配置文件中的主节点, 如tsf,tke等
        : SecretId     腾讯云SecretId
        : SecretKey    腾讯云SecretKey
        : endpoint     腾讯云接口调用地址
        """
        global SecretId,SecretKey,tce_region,endpoint
        try:
            # 判断是否存在yaml配置文件
            if os.path.exists(YamlPath):
                with open(YamlPath, 'r', encoding='utf-8') as file:
                    config=yaml.safe_load(file)
                SecretId=config[MainNode]['SecretId']
                SecretKey=config[MainNode]['SecretKey']
                tce_region=config[MainNode]['tce_region']
                endpoint=config[MainNode]['endpoint']
                return SecretId,SecretKey,tce_region,endpoint
            else:
                return False
        except Exception as err:
            return err
    
    def CheckFileSplit(self):
        '''
        路径拼接函数
        windows下用\\拼接
        linux下用/拼接
        '''
        if sys.platform.startswith('win'):
            return '\\'
        elif sys.platform.startswith('linux'):
            return '/'
        else:
            print('无法确定当前操作系统')
            exit(-1)

    def cos_CreateClient(self):
        """
        :初始化httpProfile
        :创建 cos_client 并 return .
        """
        try:
            token = None  # 使用临时密钥需要传入Token，默认为空,可不填
            config = CosConfig(Region=tce_region, SecretId=SecretId, SecretKey=SecretKey, Token=token,Endpoint=endpoint)  # 获取配置对象
            client = CosS3Client(config)
            return client
        except Exception as err:
            return err
        
    def cos_GetBucket(self):
        r"""
        获取存储桶列表
        暂定只 return 列表中第一个BucketName
        """
        client = self.cos_CreateClient()
        response = client.list_buckets()
        # {'Owner': {'ID': 'qcs::cam::uin/100027375645:uin/100027375645', 'DisplayName': '100027375645'}, 'Marker': '0', 'NextMarker': None, 'IsTruncated': 'false', 'Buckets': {'Bucket': [{'Name': 'csp-1313916223', 'Location': 'ap-guangzhou', 'CreationDate': '2024-01-20T02:33:15Z', 'BucketType': 'cos'}]}}
        return response["Buckets"]["Bucket"][0]["Name"]

    def cos_UploadFile(self,LocalFilePath,Flooder_Path=None,Bucket=None,PartSize=None,MAXThread=None):
        r"""文件分块上传腾讯云COS存储接口.   
        :LocalFilePath: 本地文件路径.
        :Flooder_Path: COS存放的文件夹路径
        :Key: 上传COS后的文件名称  默认不修改 
        :param LocalFilePath(string): 本地文件路径名.
        :param PartSize(int): 分块的大小设置,单位为MB.  默认1M
        :param MAXThread(int): 并发上传的最大线程数.    默认5T
        """
        client = self.cos_CreateClient()
        Flooder_Path=Flooder_Path.replace('\\','/') or '/'
        filename=os.path.basename(LocalFilePath)
        PartSize=PartSize or 1
        MAXThread=MAXThread or 5
        Bucket=Bucket or self.cos_GetBucket()
        try:
            if os.path.exists(LocalFilePath):
                print('开始上传文件到{}'.format(Bucket) ,'文件名称:',filename)
                response = client.upload_file(
                    Bucket=Bucket,
                    LocalFilePath=LocalFilePath,
                    Key=Flooder_Path+'/'+filename,
                    PartSize=PartSize,
                    MAXThread=MAXThread,
                )
                return response["x-cos-request-id"]
            else:
                print('未能找到文件:{},请确认!!!'.format(LocalFilePath))
                return False
        except Exception as err:
            return err
        
    def cos_DownloadFile(self,Key,Bucket=None,DestFilePath=None):
        r"""
        :小于等于20MB的文件简单下载，大于20MB的文件使用续传下载
        :param Key: COS中要下载的文件名称
        :param Bucket: 存储桶名称
        :param DestFilePath: 保存到本地文件夹的路径
        """
        try:
            CheckFileSplit=self.CheckFileSplit()
            Bucket=Bucket or self.cos_GetBucket()
            DestFilePath=DestFilePath+CheckFileSplit+Key or './'+Key
            client = self.cos_CreateClient()
            client.download_file(
                Bucket=Bucket,
                Key=Key,
                DestFilePath=DestFilePath
            )
            return '文件成功下载并储存至 {}'.format(DestFilePath)
        except Exception as err:
            print('文件下载失败.')
            return err

if __name__=="__main__":
    COSSdkCientRequest=COSSdkClient()
    COSSdkCientRequest.ReadYaml(YamlPath='./config.yaml',MainNode='cos')
    res=COSSdkCientRequest.cos_UploadFile(LocalFilePath='D:\TencentCloudSVN\TencentCloud\TCloudSDK\config.yaml',Flooder_Path=r'/data/')
    print(res)