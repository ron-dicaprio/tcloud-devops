#-*- coding:utf-8 -*-
import os, requests, json, time

global function_choice, repo_addr, distribute_addr, package_type , domain
# Todo list
# get repo_addr result by choice 
# 初始化参数
repo_addr='ysc_xdzswj'
domain='http://cpack.xc11.uat-sat.com'

# RepoName = "docker-" + name if repotype == 'DOCKER' else "generic-" + name

# get task list 
def get_history_task():
	# 取最近20个任务
	# This website do not need auth
	weburl='%s/web/replication/api/task/page/%s?sortType=CREATED_TIME&pageNumber=1&pageSize=20' % (domain,repo_addr)
	res=requests.get(weburl)
	return res.text

#res_info={'code': 0, 'message': None, 'data': {'pageNumber': 1, 'pageSize': 20, 'totalRecords': 2, 'totalPages': 1, 'records': [{'id': '6482dc480a92ab155dc2dbc6', 'key': 'f898fccbfd3d4d8c96edceb38a0f7f16', 'name': 'generic-ywzc', 'projectId': 'ysc-xdzswj', 'replicaObjectType': 'PATH', 'replicaType': 'SCHEDULED', 'setting': {'rateLimit': 0, 'includeMetadata': True, 'conflictStrategy': 'SKIP', 'errorStrategy': 'CONTINUE', 'executionStrategy': 'IMMEDIATELY', 'executionPlan': {'executeImmediately': True, 'executeTime': None, 'cronExpression': None}}, 'remoteClusters': [{'id': '64817ddc0a92ab155dc2d6ae', 'name': '青海独立'}, {'id': '64817d9e0a92ab155dc2d6ad', 'name': '山东独立'}], 'description': '', 'lastExecutionStatus': 'SUCCESS', 'lastExecutionTime': '2023-06-09T16:01:16.477', 'nextExecutionTime': None, 'executionTimes': 0, 'enabled': True, 'createdBy': 'admin', 'createdDate': '2023-06-09T16:01:12.797', 'lastModifiedBy': 'admin', 'lastModifiedDate': '2023-06-09T16:01:12.797'}, {'id': '6477f93d0a92ab155dc2c30d', 'key': 'b743b27741874d4e9cb1733f5c98b6b3', 'name': '四川-全量制品实时同步-0601', 'projectId': 'ysc-xdzswj', 'replicaObjectType': 'REPOSITORY', 'replicaType': 'REAL_TIME', 'setting': {'rateLimit': 0, 'includeMetadata': True, 'conflictStrategy': 'SKIP', 'errorStrategy': 'CONTINUE', 'executionStrategy': 'IMMEDIATELY', 'executionPlan': {'executeImmediately': True, 'executeTime': None, 'cronExpression': None}}, 'remoteClusters': [{'id': '634a5efdbb557f138d30689d', 'name': '四川独立'}], 'description': '', 'lastExecutionStatus': 'RUNNING', 'lastExecutionTime': None, 'nextExecutionTime': None, 'executionTimes': 0, 'enabled': True, 'createdBy': 'admin', 'createdDate': '2023-06-01T09:49:48.969', 'lastModifiedBy': 'admin', 'lastModifiedDate': '2023-06-01T09:49:48.969'}], 'count': 2,'page': 1}, 'traceId': ''}
	
def del_history_task():
	res_info=json.loads(get_history_task())
	#res_info['data']['records'][i]['key']
	lenth=len(res_info['data']['records'])
	print(lenth)
	for index in range(0,lenth):
		del_key=res_info['data']['records'][index]['key']
		# if status is running , pass . else delete  history task.
		if res_info['data']['records'][index]['lastExecutionStatus']=='RUNNING':
			print('task %s is running, pass ...' % (del_key))
			print(res_info['data']['records'][index]['remoteClusters'])
			pass
		else:
			del_url='%s/replication/api/task/delete/%s' % (domain,del_key)
			print(del_url)
			res=requests.delete(del_url,auth=('zrdzfp','bkrepo123456'))
			print(res.text)

def create_sync_task(app_name):
	app_version=search_last_imgver(app_name)
	weburl='%s/replication/api/task/create' % (domain)
	header={"Content-Type":"application/json"}
	RepoName = "docker-" + app_name
	params = {
		"name": app_name + "-" + time.strftime("%H%M"),
		"localProjectId": "ysc-xdzswj",
		"replicaObjectType": "PACKAGE",
		"replicaTaskObjects": [
			{
				"localRepoName": RepoName,
				"remoteProjectId": "ysc-xdzswj",
				"remoteRepoName": RepoName,
				"repoType": "DOCKER",
				"packageConstraints": [
					{
						"packageKey": "docker://yscsj-%s" % (app_name),
						"versions": [
							app_version
						]
					}
				]
			}
		],
		"replicaType": "SCHEDULED",
		"setting": {
			"rateLimit": 0,
			"includeMetadata": "true",
			"conflictStrategy": "SKIP",
			"errorStrategy": "CONTINUE",
			"executionStrategy": "IMMEDIATELY",
			"executionPlan": {
				"executeImmediately": "true"
			}
		},
		#自行选择分发地址 remoteClusterIds
		#[{'id': '634a5efdbb557f138d30689d', 'name': '四川独立'}]
		#[{'id': '639716fc022a5c6038c2b6c6', 'name': '陕西独立'}]
		#[{'id': '6397175c588a4a7c6dc9cb93', 'name': '天津独立'}]
		"remoteClusterIds": [
			"634a5efdbb557f138d30689d"
		],
		"enabled": "true",
		"description": ""
	}
	params=json.dumps(params)
	print("--开始分发镜像%s:%s--" % (app_name,app_version))
	res=requests.post(weburl,headers=header, data=params,auth=('zrdzfp','bkrepo123456'))
	# 防止蓝鲸接口被弄挂  休息两秒继续干
	time.sleep(2)
	print(res.text)
	print("--镜像分发完毕%s:%s--" % (app_name,app_version))
	

def search_last_imgver(app_name):
	header={"Content-Type":"application/json"}
	weburl='%s/repository/api/package/search' % (domain)
	payloads={
	"page": {
		"pageNumber": 1,
		"pageSize": 20
	},
	"sort": {
		"properties": [
		"lastModifiedDate"
		],
		"direction": "ASC"
	},
	"rule": {
		"rules": [
		{
			"field": "projectId",
			"value": "ysc-xdzswj",
			"operation": "EQ"
		},
		{
			"field": "repoType",
			"value": "DOCKER",
			"operation": "EQ"
		},
		{
			"field": "name",
			"value": "*%s" % (app_name),
			"operation": "MATCH"
		}
		],
		"relation": "AND"
	}
	}
	payloads=json.dumps(payloads)
	res=requests.post(weburl,headers=header,data=payloads,auth=('zrdzfp','bkrepo123456'))
	#if len(res.text['data']['records']) > 0:
	return json.loads(res.text)['data']['records'][1]['latest']
		
def sync_script_task(app_name):
	weburl='%s/replication/api/task/create' % (domain)
	header={"Content-Type":"application/json"}
	RepoName = "generic-" + app_name
	#"name": app_name + "-" + time.strftime("%m%d%H%M"),
	params = {
	  "name": app_name + "-" + time.strftime("%H%M"),
	  
	  "localProjectId": "ysc-xdzswj",
	  "replicaObjectType": "PATH",
	  "replicaTaskObjects": [
		{
		  "localRepoName": RepoName,
		  "remoteProjectId": "ysc-xdzswj",
		  "remoteRepoName": RepoName,
		  "repoType": "GENERIC",
		  "pathConstraints": [
			{
			  "path": "/"
			}
		  ]
		}
	  ],
	  "replicaType": "SCHEDULED",
	  "setting": {
		"rateLimit": 0,
		"includeMetadata": "true",
		"conflictStrategy": "SKIP",
		"errorStrategy": "CONTINUE",
		"executionStrategy": "IMMEDIATELY",
		"executionPlan": {
		  "executeImmediately": "true"
		}
	  },
		#自行选择分发地址remoteClusterIds
		#[{'id': '634a5efdbb557f138d30689d', 'name': '四川独立'}]
		#[{'id': '639716fc022a5c6038c2b6c6', 'name': '陕西独立'}]
		#[{'id': '6397175c588a4a7c6dc9cb93', 'name': '天津独立'}]
		# 64817ddc0a92ab155dc2d6ae
	  "remoteClusterIds": [
		"634a5efdbb557f138d30689d"
	  ],
	  "enabled": "true",
	  "description": ""
	}
	params=json.dumps(params)
	print("--开始分发脚本generic-%s--" % (app_name))
	res=requests.post(weburl,headers=header, data=params,auth=('admin','password'))
	# 防止蓝鲸接口被弄挂  休息两秒继续干
	time.sleep(2)
	print(res.text)
	print("--脚本分发完毕generic-%s--" % (app_name))

#删除已经执行成功的历史任务
#del_history_task()

#创建微服务最新版本镜像的同步任务 不需要带yscsj-
#create_sync_task('skzs-front-jd-web')
#create_sync_task('skzs-front-nsrd-web')
create_sync_task('cxssb-service')
create_sync_task('cxssb-front-nsrd-web')


#获取当前列表中的存量任务
#print(get_history_task())

#同步的脚本 不需要带yscsj-
#sync_script_task('dksq-service')


