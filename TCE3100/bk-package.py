# -*- coding:utf-8 -*-
import os,requests,json,time

# def global items
global app_list,app_list_gen
app_list=["yyzx-ctrl-jd",
    "yyzx-service",
    "cxssb-front-jd-web",
    "xwcjsjjg-service",
    "yyzx-front-jd-web",
    "cxssb-ctrl-jd",
    "cxssb-service",
    "cxssb-web-jd",
    "dksq-ctrl-jd",
    "dksq-service",
    "dksq-front-jd-web",
    "jcaj-front-jd-web",
    "jcaj-service",
    "jcaj-ctrl-jd",
    "j3cx-service",
    "jcsb-service",
    "mh-ctrl-jd",
    "mh-service-jd",
    "mh-service",
    "mh-front-jd-web",
    "nsrxx-service",
    "skzs-ctrl-jd",
    "skzs-service",
    "skzs-front-jd-web",
    "sqsp-service",
    "wfcz-service",
    "wfwwg-service",
    "xxzx-ctrl-jd",
    "xxzxnsrd-service",
    "xxzxjd-service",
    "xxzx-front-jd-web",
    "ztxxbg-ctrl-jd",
    "ztxxbg-service",
    "ztxxbg-front-jd-web",
    "ztzx-ctrl-jd",
    "ztzx-service",
    "ztzx-front-jd-web",
    "xwcjsjjs-ctrl-nsrd",
    "cxssb-ctrl-nsrd",
    "cxssb-front-nsrd-web",
    "ckts-ctrl-nsrd",
    "ckts-front-nsrd-web",
    "dksq-ctrl-nsrd",
    "dksq-front-nsrd-web",
    "jcaj-front-nsrd-web",
    "jcaj-ctrl-nsrd",
    "mh-ctrl-nsrd",
    "mh-front-nsrd-web",
    "skzs-ctrl-nsrd",
    "skzs-front-nsrd-web",
    "xxzx-ctrl-nsrd",
    "xxzx-front-nsrd-web",
    "ztxxbg-ctrl-nsrd",
    "ztxxbg-front-nsrd-web",
    "ztzx-ctrl-nsrd",
    "ztzx-front-nsrd-web"]

app_list_gen=["yyzx-ctrl-jd",
    "yyzx-service",
    "xwcjsjjg-service",
    "yyzx-front-jd-web",
    "cxssb-ctrl-jd",
    "cxssb-service",
    "cxssb-web-jd",
    "dksq-ctrl-jd",
    "dksq-service",
    "jcaj-service",
    "jcaj-ctrl-jd",
    "j3cx-service",
    "jcsb-service",
    "mh-ctrl-jd",
    "mh-service-jd",
    "mh-service",
    "nsrxx-service",
    "skzs-ctrl-jd",
    "skzs-service",
    "sqsp-service",
    "wfcz-service",
    "wfwwg-service",
    "xxzx-ctrl-jd",
    "xxzxnsrd-service",
    "xxzxjd-service",
    "ztxxbg-ctrl-jd",
    "ztxxbg-service",
    "ztzx-ctrl-jd",
    "ztzx-service",
    "jcaj-ctrl-jd"]

# 创建业务拓扑 done
def create_yw_top():
    # 创建业务拓扑url
    weburl="http://cmdb.ywpt.hesw.tax/api/v3/module/19/44"
    chrome_header={
        "Content-Type": "application/json",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Cookie":'''http_scheme=http; blueking_language=zh-cn; bk_token=7kuHTPasqe0yOyk7LiA1kKOTldHhow0eB4fAkMDYvAI; cc3=MTcwMzA0MTM4OHxOd3dBTkZFeVNGWktURFJUVFVWQlQxcEVWVlpQTmtKR1JEUlRSVTFJTlZGVlN6UTFXVWRKVjB4SU5VOVNUMXBFV2taWFdsZFNURkU9fHykCzvVP9z8_Nc8JsnL3o4cBAgoZo7d2SKiHSGm0J-X'''
        }
        
    # 循环创建
    for app_name in app_list:
        payload={
        "bk_module_name": "scsj-%s" % (app_name),
        "service_category_id": 2,
        "service_template_id": 0,
        "bk_biz_id": 19,
        "bk_parent_id": 44
        }
        res=requests.post(weburl,headers=chrome_header,data=json.dumps(payload))
        # result is not unique . so fuck BK.
        if json.loads(res.text)["result"]=='true' or json.loads(res.text)["result"] is True:
            print(app_name,":创建业务拓扑完毕")
        else:
            print(app_name,":创建业务拓扑失败", json.loads(res.text))
        # 暂停两秒
        time.sleep(2)


# 创建程序包
def create_img_pack():
    # 创建程序包url
    weburl="http://bkpaas.ywpt.hesw.tax/o/app-mgmt_saas/package/add_package"
    chrome_header={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "X-CSRFToken": "G19rEaQIUfFtsmd8QQIaUIZnK93zGh5E8CfpHO0okIuwqBeFJPxJX27tIE7BIqiL",
        "Cookie": '''sessionid=lq26htnjfyrxvidpm4addx30s26b16h0; bk_csrftoken=T7MiBuOmEEKnIyv1EvqXfyZ7fyJIrdT0I5b1YBs8WVMoKG2GgtmGZVuVwPFfYXL3; bk_sops_sessionid=b1i5sfcfutnkorxl5b6xlvnuo3heyk0i; cw-publish_saas_csrftoken=LvSGCoAsQn1uaObFgYSlOW0C72suCUYZlIJqlq0KYmeGEtgKjGpyW6xYhxXoR0sE; cw-publish_saas_sessionid=55553uypxiqai6i4afrxi7xodxy2xx9o; app-mgmt_saas_csrftoken=G19rEaQIUfFtsmd8QQIaUIZnK93zGh5E8CfpHO0okIuwqBeFJPxJX27tIE7BIqiL; app-mgmt_saas_sessionid=6eaytyxkijdfmyshiakxcbr00fgtvha4; r_s={"lock":false,"msg":{}}; bk_sops_csrftoken=xRpbI7rLfZ5uj2r5PiUkVKALMMNhJUil6SSjEvPAHlQV298cYF75BEKYYWuVj3HK; blueking_language=zh-cn; bk_token=7kuHTPasqe0yOyk7LiA1kKOTldHhow0eB4fAkMDYvAI; bklogin_csrftoken=ott0XZh59CVkj2GeTUEuhbT7otZ0uvDYVhXfDaXDfpyRZztZST4Ybt55ECMTsxJn; r_f={"lock":true,"msg":{"workbench":14}}; csrftoken=URTRvH7AM3y9MyBBhdmdqZzj3YKzyhj2msZPylhgcwncKNC8acbMtjHp1tOBAqw9; o_s={"lock":true,"msg":{}}; o_f={"lock":false,"msg":{}}'''
        }
    for app_name in app_list:
        payload={
        "name": "docker-scsj-%s" % (app_name),
        "appcode_only": "docker-scsj-%s" % (app_name),
        "type": "images",
        "dis": "",
        "source": "product_library",
        "moduleId": [
        ],
        "groups_id_list": [
            14,
            13
        ],
        "biz_id": "",
        "set": "",
        "now_product": 4,
        "productSettings": [
            {
            "id": 15,
            "productlibrary_id": 3,
            "en_name": "project",
            "cn_name": "项目名",
            "type": "text",
            "where": "package",
            "des": "cpack项目名称",
            "is_exists": "true",
            "val": "sc-xdzswj"
            },
            {
            "id": 16,
            "productlibrary_id": 3,
            "en_name": "repo",
            "cn_name": "仓库名",
            "type": "text",
            "where": "package",
            "des": "cpack仓库名称",
            "is_exists": "true",
            "val": "docker-%s" % (app_name)
            },
            {
            "id": 17,
            "productlibrary_id": 3,
            "en_name": "package",
            "cn_name": "制品名",
            "type": "text",
            "where": "package",
            "des": "cpack制品名称",
            "is_exists": "true",
            "val": "scsj-%s" % (app_name)
            },
            {
            "id": 18,
            "productlibrary_id": 3,
            "en_name": "repo_type",
            "cn_name": "仓库类型",
            "type": "text",
            "where": "package",
            "des": "仓库类型",
            "is_exists": "true",
            "val": "DOCKER"
            },
            {
            "id": 19,
            "productlibrary_id": 3,
            "en_name": "path",
            "cn_name": "文件夹路径",
            "type": "text",
            "where": "package",
            "des": "仓库类型",
            "is_exists": "true",
            "val": "/"
            }
        ]
        }
        res=requests.post(weburl,headers=chrome_header,data=json.dumps(payload))
        # result is not unique . so fuck BK.
        if json.loads(res.text)["result"]=='true' or json.loads(res.text)["result"] is True:
            print(app_name,":创建image程序包完毕")
        else:
            print(app_name,":创建image程序包失败", json.loads(res.text))
        # 暂停两秒
        time.sleep(2)


# 创建程序包
def create_tar_pack():
    # 创建程序包url
    weburl="http://bkpaas.ywpt.hesw.tax/o/app-mgmt_saas/package/add_package"
    chrome_header={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "X-CSRFToken": "Ymgf5TNxCoPpG6IF093TUkjSMCp4neugpHu6IJ3A4KDWqiwvhq8dhBkSsseCwzXy",
        "Cookie": '''bk_csrftoken=7pbwlc316rLK95ArUkwRhmyqWOZRM8bX5M6fzVujdwv7VrMVe13VflaXejJdCinC; bkuser_csrftoken=KRZas6xjQsfLrnt8xkFYxYpejUYEioZ7JCNmJDmsjF6ueHLYUYgAfGwIyQbkpUK9; r_s={"lock":false,"msg":{}}; blueking_language=zh-cn; bkiam_csrftoken_964527466667c34d=ESFKOhApecnvrfYl2H1IOrcS70rO2Qp00fXptmV36JnS2zNzIwYPP4PSpzknw1Ew; bkiam_sessionid=fp9lo95lakriddq4nkt26rytnjqqkp40; bk_token=0CP15NoVfzC2Shg80Hjupj8K7ew414Vt2T70QFYVI84; bklogin_csrftoken=enre11ETI9OsypxGVWR0wCt59RjvdyjzPKL9kxGYwnw2X7GEQNAICp5uF1UHxK37; sessionid=qwp9iyz0lk2zyyzef62rh1ymq4qpv9gj; backend-apis_saas_csrftoken=ycCud5zBguKfFfTREGoMV05nhPJa8fuaJrHJVx7oYHCaZdkAjSvGezP6YRnAhi9M; backend-apis_saas_sessionid=b08c1efmyvg1qiyk4djw01tq8mq5jpx7; app-mgmt_saas_csrftoken=Ymgf5TNxCoPpG6IF093TUkjSMCp4neugpHu6IJ3A4KDWqiwvhq8dhBkSsseCwzXy; app-mgmt_saas_sessionid=hlojuh0o1iksljctrgbn3a4ol8hcmw51; cw-publish_saas_csrftoken=jIkUiHs1c3OYrCHXkqZCyWv2JcPYox2BZPS0zXd2yVshdw2EbG0Ez4S55M3DgOua; cw-publish_saas_sessionid=sfaui5x301hr3j14joy69slb9az3e6m0; bk_sops_csrftoken=pzE5GseAj22pj0M2lHbGGCzFjPeHE01zqZ6iwBNunhSlfQk4nyTzTH6yalHEGrOa; bk_sops_sessionid=fpgdo9nxel1tzlmqqk0x4t1t1e3roiyu; r_f={"lock":true,"msg":{"workbench":36}}; o_f={"lock":true,"msg":{}}; o_s={"lock":false,"msg":{}}; csrftoken=n1xTvMAGSy4g2jY6f00pHeUl6fYpKYQpOmLK8CQJkUSNMvMWwh5J4vVlM5NXTjjH'''
        }
    for app_name in app_list_gen:
        payload={
        "name": "generic-scsj-%s" % (app_name),
        "appcode_only": "generic-scsj-%s" % (app_name),
        "type": "tar",
        "dis": "",
        "source": "product_library",
        "moduleId": [
            [
            "19",
            "44",
            "324"
            ]
        ],
        "groups_id_list": [
            13,
            14
        ],
        "biz_id": "",
        "set": "",
        "now_product": 4,
        "productSettings": [
            {
            "id": 15,
            "productlibrary_id": 3,
            "en_name": "project",
            "cn_name": "项目名",
            "type": "text",
            "where": "package",
            "des": "cpack项目名称",
            "is_exists": "true",
            "val": "sc-xdzswj"
            },
            {
            "id": 16,
            "productlibrary_id": 3,
            "en_name": "repo",
            "cn_name": "仓库名",
            "type": "text",
            "where": "package",
            "des": "cpack仓库名称",
            "is_exists": "true",
            "val": "generic-%s" % (app_name)
            },
            {
            "id": 17,
            "productlibrary_id": 3,
            "en_name": "package",
            "cn_name": "制品名",
            "type": "text",
            "where": "package",
            "des": "cpack制品名称",
            "is_exists": "true",
            "val": "scsj-%s" % (app_name)
            },
            {
            "id": 18,
            "productlibrary_id": 3,
            "en_name": "repo_type",
            "cn_name": "仓库类型",
            "type": "text",
            "where": "package",
            "des": "仓库类型",
            "is_exists": "true",
            "val": "GENERIC"
            },
            {
            "id": 19,
            "productlibrary_id": 3,
            "en_name": "path",
            "cn_name": "文件夹路径",
            "type": "text",
            "where": "package",
            "des": "仓库类型",
            "is_exists": "true",
            "val": "/"
            }
        ]
        }

        res=requests.post(weburl,headers=chrome_header,data=json.dumps(payload))
        # result is not unique . so fuck BK.
        if json.loads(res.text)["result"]=='true' or json.loads(res.text)["result"] is True:
            print(app_name,":创建tar程序包完毕")
        else:
            print(app_name,":创建tar程序包失败", json.loads(res.text))
        # 暂停两秒
        time.sleep(2)

# 创建入口
if __name__=="__main__":
    print('start!')
    #create_yw_top()
    #create_img_pack()
    #create_tar_pack()
