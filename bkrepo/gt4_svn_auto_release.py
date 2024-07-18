import requests,json,time,os,zipfile

def del_history_task():
	res_info=json.loads(requests.get('http://cpack.xc11.uat-sat.com/web/replication/api/task/page/ysc-xdzswj?sortType=CREATED_TIME&pageNumber=1&pageSize=8').text)
	#res_info['data']['records'][i]['key']
	lenth=len(res_info['data']['records'])
	for index in range(0,lenth):
		del_key=res_info['data']['records'][index]['key']
		# if status is running , pass . else delete  history task.
		if res_info['data']['records'][index]['lastExecutionStatus']=='SUCCESS':
			del_url='http://cpack.xc11.uat-sat.com/replication/api/task/delete/%s' % (del_key)
			requests.delete(del_url,auth=('bkuser','bkpass'))
		else:
			print('task %s is not SUCCESS, pass ...' % (del_key))
	
ProviceLists=None
def GetCpackProviceIDList(provice_names:list):
	global ProviceLists
	if ProviceLists:
		print("Requeste exsist.")
	else:
		try:
			ysc_cpackurl="http://cpack.xc11.uat-sat.com/api/replication/api/cluster/list"
			res=requests.get(ysc_cpackurl,auth=('bkuser','bkpass')).text
			ProviceLists=json.loads(res)["data"]
			proviceListID=[]
			for provice_name in provice_names:
				for item in ProviceLists:
					if item.get("name")==provice_name:
						proviceListID.append(item.get("id"))
			return proviceListID
		except Exception as err:
			print(err)
			return False

# svn checkout
def Checkout_Versions():
	try:
		os.system("svn update E:\\swrd\\swrd_versions_svn\\01出厂版本\\税务人端出厂汇总表.xls")
		os.system("svn update E:\\zr_lyt\\gt4_xdzswj\\01出厂版本\\电子税务局出厂汇总表.xls")
		os.system("svn update E:\\zr_lyt\\gt4_xdzswj_app\\01出厂版本\\电子税务局APP出厂汇总表.xls")
		with zipfile.ZipFile("E:\\zr_cait\\DO-NOT-DELETE\\auto_release.zip","w") as zip_ref:
			zip_ref.write("E:\\swrd\\swrd_versions_svn\\01出厂版本\\税务人端出厂汇总表.xls","税务人端出厂汇总表.xls")
			zip_ref.write("E:\\zr_lyt\\gt4_xdzswj\\01出厂版本\\电子税务局出厂汇总表.xls","电子税务局出厂汇总表.xls")
			zip_ref.write("E:\\zr_lyt\\gt4_xdzswj_app\\01出厂版本\\电子税务局APP出厂汇总表.xls","电子税务局APP出厂汇总表.xls")
		with open("E:\\zr_cait\\DO-NOT-DELETE\\auto_release.zip","rb") as file_ref:
			res1=requests.delete("http://cpack.xc11.uat-sat.com/api/repository/api/node/delete/ysc-xdzswj/xdzswj-add-service/auto_release.zip",auth=("bkuser","bkpass"))
			#print(res1.text)
			res2=requests.put("http://cpack.xc11.uat-sat.com/api/generic/ysc-xdzswj/xdzswj-add-service/auto_release.zip",files={"file": file_ref}, auth=("bkuser","bkpass"))
			#print(res2.text)
		return True
	except Exception as err:
		print(err)
		return False
	
#remoteClusterIds could be a list
def sync_script_task(provice_names:list):
	weburl='http://cpack.xc11.uat-sat.com/replication/api/task/create'
	header={"Content-Type":"application/json"}
	#"name": app_name + "-" + time.strftime("%m%d%H%M"),
	remoteClusterIds=GetCpackProviceIDList(provice_names)
	params = {
	  "name": "xdzswj-add-service" + "-" + time.strftime("%H%M"),
	  "localProjectId": "ysc-xdzswj",
	  "replicaObjectType": "PATH",
	  "replicaTaskObjects": [
		{
		  "localRepoName": "xdzswj-add-service",
		  "remoteProjectId": "ysc-xdzswj",
		  "remoteRepoName": "xdzswj-add-service",
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
		"conflictStrategy": "OVERWRITE",
		"errorStrategy": "CONTINUE",
		"executionStrategy": "IMMEDIATELY",
		"executionPlan": {
		  "executeImmediately": "true"
		}
	  },
		"remoteClusterIds": remoteClusterIds,
	  "enabled": "true",
	  "description": ""
	}
	params=json.dumps(params)
	print("--开始分发脚本--")
	requests.post(weburl,headers=header, data=params,auth=('bkuser','bkpass'))
	# 防止Cpack接口被弄挂  休息两秒继续干
	time.sleep(2)
	#print(res.text)
	print("--脚本分发完毕--")

del_history_task()

if Checkout_Versions():
	sync_script_task(["湖南独立","四川独立","广东独立(新)","河北独立","新疆独立","陕西独立"])