import boto3,os,yaml,sys
# Get configurations
def ReadYaml(YamlPath: str, MainNode: str ):
    r"""
    :Get configuration with PyYAML.
    """
    try:
        # Validate the configuration file.
        if os.path.exists(YamlPath):
            with open(YamlPath, 'r', encoding='utf-8') as file:
                config=yaml.safe_load(file)
            s3_url=config[MainNode]['s3_url']
            aws_access_key_id=config[MainNode]['aws_access_key_id']
            aws_secret_access_key=config[MainNode]['aws_secret_access_key']
            return s3_url,aws_access_key_id,aws_secret_access_key
        else:
            print('resove filepath error. please check !')
            sys.exit(1)
    except Exception as err:
        print('resove file error. please check !', err)
        sys.exit(1)
# S3StorageRequest Operation Class
class S3SdkClient():
    r"""
    :init s3_url, aws_access_key_id, aws_secret_access_key
    """
    def __init__(self,s3_url,aws_access_key_id,aws_secret_access_key):
        self.s3_url=s3_url
        self.aws_access_key_id=aws_access_key_id
        self.aws_secret_access_key=aws_secret_access_key
    # Create S3 Client
    def CreateS3Clinet(self):
        S3Client = boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key,endpoint_url=self.s3_url)
        return S3Client
    # Create S3 Bucket
    def CreateBucket(self,S3Client,bucket_name):
        res=S3Client.create_bucket(Bucket=bucket_name)
        return res
    # List Buckets
    def ListS3Bucket(self,S3Client):
        bucket_list=[]
        response = S3Client.list_buckets()
        for bucket in response['Buckets']:
            bucket_list.append(bucket['Name'])
        return bucket_list
    # List All Files From Bucket
    def ListBucketFile(self,S3Client,bucket_name):
        response = S3Client.list_objects_v2(Bucket=bucket_name)
        FileList=[]
        for obj in response.get('Contents', []):
            FileList.append(obj['Key'])
        return FileList
    # Upload File To S3 Bucket
    # add try except
    def UploadS3File(self,S3Client,bucket_name,LocalFilepath,UploadFileName,UploadFolder=None):
        UploadFilePath = UploadFolder + "/" + UploadFileName if UploadFolder else UploadFileName
        if os.path.exists(LocalFilepath):
            S3Client.upload_file(LocalFilepath, bucket_name, UploadFilePath)
            return True
        else:
            print(f"File {LocalFilepath} not exist .")
            return False
    # Delete File From S3 Bucket
    def DeleteS3File(self,S3Client,bucket_name,FileName):
        res=S3Client.delete_object(Bucket=bucket_name, Key=FileName)
        return res
    # Dowenload File
    # Should Verify Linux Or Windows OS
    def DownloadS3File(self,S3Client,bucket_name,s3_file_key,LocalFilepath=None):
        LocalFilepath=LocalFilepath + "/" + s3_file_key if LocalFilepath else s3_file_key
        res=S3Client.download_file(bucket_name, s3_file_key, LocalFilepath)
        return res

if __name__=="__main__":
    s3_url, aws_access_key_id, aws_secret_access_key = ReadYaml("./CloudFlareR2Config.yaml","R2")
    S3StorageRequest=S3SdkClient(s3_url,aws_access_key_id,aws_secret_access_key)
    S3StorageClient=S3StorageRequest.CreateS3Clinet()
    #print(S3StorageRequest.ListS3Bucket(S3StorageClient))
    # s3bucket
    #print(S3StorageRequest.UploadS3File(S3StorageClient,"s3bucket","./CloudFlareR2Config.yaml","CloudFlareR2Config.yaml",UploadFolder=None))
    print(S3StorageRequest.DeleteS3File(S3StorageClient,"s3bucket","CloudFlareR2Config.yaml"))
