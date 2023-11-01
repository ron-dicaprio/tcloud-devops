# -*- coding:utf-8 -*-
import pandas,os
# 初始化数据  增加一列#app_name并赋值
def get_appname():
    try:
        all_dataframe=pandas.read_excel('电子税务局出厂汇总表.xls',sheet_name=0,header=0)
        app_name_list=[]
        for i in range(0,len(all_dataframe)):
            app_name=str(all_dataframe.iat[i,1])[42:]
            app_name_list.append(app_name)
        #print(app_name_list)
        all_dataframe.insert(loc=8, column='#app_name', value=app_name_list)
        all_dataframe.to_excel('电子税务局出厂汇总表.xls', index=False)
        return True
    except Exception as E:
        return E

def search_appinfo():
    all_dataframe=pandas.read_excel('电子税务局出厂汇总表.xls',sheet_name=0,header=0)
    search_dataframe=pandas.read_excel('res.xls',sheet_name=0,header=0)
    for i in range(0,len(search_dataframe)):
        app_name=search_dataframe.iat[i,1]
        app_version=search_dataframe.iat[i,2]
        # 双重判断
        condition = (all_dataframe['#app_name'] == app_name) & (all_dataframe['#docker_ver'] == app_version)
        matching_rows=all_dataframe[condition]
        if not matching_rows.empty:
            # 如果只匹配到一行
            if len(matching_rows)==1:
                row = matching_rows.iloc[0]
                res_remark=row['#note']
                print(res_remark)
                search_dataframe.iat[i,3]=row['#ver']
                if 'script' in str(res_remark):
                    search_dataframe.iat[i,4]='存在脚本'
                else:
                    search_dataframe.iat[i,4]='无脚本'
                if 'yaml' in str(res_remark):
                    search_dataframe.iat[i,5]='存在特殊说明'
                else:
                    search_dataframe.iat[i,5]='无特殊说明'
            # 如果只匹配到多行
            if len(matching_rows)>1:
                mult_res=[]
                for n in range(0,len(matching_rows)):
                   mult_res.append(matching_rows.iloc[n]['#ver'])
                search_dataframe.iat[i,3]=str(mult_res)
        else:
            print('match error!')
    # 写入excel中
    search_dataframe.to_excel('res.xls', index=False)

if __name__=='__main__':
    res = get_appname()
    if res == True:
        search_appinfo()
    else:
        print(res)
