#-*- encoding:utf-8 -*-
# bktools.py v1.0
import requests
def GetTokens(domain,username,password,hostip=None):
    """
    通过这个函数获取cookies里面所需的token
    如果存在无权限修改hosts的情况 定义hostip来解析域名
    paramas: domain="bkpaas.ywpt.xjsw.tax"
    paramas: username="demo_user"
    paramas: password="demo_passwd"
    paramas: hostip . we use host ip to resove domain.
    """
    IPResove=hostip if hostip else None
    if IPResove:
        ReqUrl=IPResove
    else:
        ReqUrl=domain
    basic_header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Host": f"{domain}"
    }
    res_csrf=requests.get(f"http://{ReqUrl}/login/?c_url=/",verify=False,timeout=(10,20),headers=basic_header)

    bklogin_csrftoken=res_csrf.cookies.get("bklogin_csrftoken")
    chrome_header={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        "Host": f"{domain}",
        "Origin": f"http://{domain}",
        "Referer": f"http://{domain}/login/?c_url=/",
        "X-csrfToken": bklogin_csrftoken, 
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f"bklogin_csrftoken={bklogin_csrftoken}",
        }

    data={
        "csrfmiddlewaretoken": bklogin_csrftoken,
        "username": username,
        "password": password,
        "next": "",
        "app_id": "", 
    }
    res_token=requests.post(url=f"http://{ReqUrl}/login/?c_url=/", data=data, headers=chrome_header,verify=False,allow_redirects=False,timeout=(10,20))
    bk_token=res_token.cookies.get("bk_token")
    bk_csrftoken=res_token.cookies.get("bklogin_csrftoken")
    return bk_csrftoken,bk_token

print(GetTokens(domain="bkpaas.ywpt.xjsw.tax",username="demo_user",password="demo_passwd",hostip="100.0.0.100"))
