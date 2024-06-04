import boto3,yaml,os,json
class DynamodbSdkClient():
    r""" 
    :Based On boto3 31.34.23 .
    :This Is A Class For AWS Dynamodb .
    """
    def __init__(self, DynamodbClient=None, TableName=None):
        """
        # todo list
        :param DynamodbClient: A Boto3 DynamoDB resource.
        """
        self.DynamodbClient = DynamodbClient
        # The table variable is set during the scenario in the call to .
        self.TableName = TableName

    def ReadYaml(self, MainNode: str ,YamlPath: str):
        r"""
        :利用PyYAML库读取配置文件 
        :注意全局变量
        :aws_access_key_id 
        :aws_secret_access_key
        """
        global aws_access_key_id,aws_secret_access_key
        try:
            # 判断是否存在yaml配置文件
            if os.path.exists(YamlPath):
                with open(YamlPath, 'r', encoding='utf-8') as file:
                    config=yaml.safe_load(file)
                aws_access_key_id=config[MainNode]['aws_access_key_id']
                aws_secret_access_key=config[MainNode]['aws_secret_access_key']
                return aws_access_key_id,aws_secret_access_key
            else:
                print('解析文件路径异常 请确认!!!')
                exit(1)
        except Exception as err:
            print('解析文件异常 请确认!!!', err)
            exit(1)

    def GetDynamodbClient(self):
        """
        # 通过访问密钥和密钥返回DynamodbClient对象
        """
        DynamodbClient = boto3.client('dynamodb', region_name='ap-northeast-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        return DynamodbClient
    
    def CreateTable(self,DynamodbClient,TableName):
        attribute_definitions = [
            {'AttributeName': 'id', 'AttributeType': 'N'},
            {'AttributeName': 'name', 'AttributeType': 'S'}
        ]
        key_schema = [
            {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'name', 'KeyType': 'RANGE'}  # Sort key (optional)
        ]
        provisioned_throughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }

        response = DynamodbClient.create_table(TableName=TableName,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput)
        return response

    def GetTableInfo(self,TableName,DynamodbClient):
        response = DynamodbClient.describe_table(TableName=TableName)
        # 提取表的描述信息
        table_description = response['Table']
        return json.dumps(table_description)
    
    def PutKeys(self, DynamodbClient, TableName):
        """
        # AttributeType（属性类型）：指定了属性值的数据类型。DynamoDB支持以下几种属性类型：
        # 'S'：字符串类型。
        # 'N'：数字类型。
        # 'B'：二进制类型。
        # 'BOOL'：布尔类型。
        # 'NULL'：空值类型。
        # 'L'：列表类型。
        # 'M'：映射类型。
        # AttributeName：指定用作主键的属性名称。
        # KeyType：指定主键的类型，可以是HASH（分区键）或RANGE（排序键）。
        """
        dynamodb=DynamodbClient
        # 向表中插入一条数据
        response = dynamodb.put_item(
            TableName=TableName,
            Item={
                'Row_ID': {'N': '1'},
                'ConfigName': {'S': 'John Doe'}
            }
        )
        return response
    
    def GetKeys(self,TableName,DynamodbClient):
        dynamodb=DynamodbClient
        # 查询表中的数据
        response = dynamodb.get_item(
            TableName=TableName,
            Key={
                'id': {'N': '1'},
                'name': {'S': 'John Doe'}
            }
        )
        return response

DynamodbSdkClientRequest=DynamodbSdkClient()
DynamodbSdkClientRequest.ReadYaml(YamlPath='./DynamodbConfig.yaml', MainNode='aws')
DynamodbClient=DynamodbSdkClientRequest.GetDynamodbClient()
res=DynamodbSdkClientRequest.GetTableInfo(DynamodbClient=DynamodbClient,TableName='infomation')
print(res)




# Table Name: info
# Status: ACTIVE
# Creation Date: 2024-01-25 12:25:29.087000+00:00
# Item Count: 0
# Provisioned Throughput:
#   Read Capacity: 5
#   Write Capacity: 5
# Key Schema:
#   AttributeName: id
#   KeyType: HASH
#   AttributeName: name
#   KeyType: RANGE

