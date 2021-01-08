import  pandas as pd
import pymysql
import datetime,time
import os
import xlrd
import numpy as np
import shutil

def find_file(path):
    os.system('mkdir xlsxfile')
    all_file = os.listdir(path)
    need_file = './xlsxfile/'
    for name in all_file:
        if name.startswith('com.') or name.startswith('surface') or name.startswith('system'):
            #找到符合条件的文件名
            new_name = os.path.splitext(name)[0]
            #文件路径
            new_path = path+new_name+'.xlsx'
            # 打开相应的文件
            shutil.copy(new_path,need_file)


def to_error_detail(path,num):
    workbook_c = xlrd.open_workbook(path+'com.hryt.desktop.xlsx')
    sheetname_c = workbook_c.sheet_names()

    dealed_path = []#删选出来文件的所有路径
    need_name = []
    for needed_name in os.listdir(path):
        need_name.append(needed_name.split('.xlsx')[0])
        needed_file = os.path.join(path,needed_name)
        dealed_path.append(needed_file)
    print(need_name)
    print(dealed_path)
    for i in range(0,len(dealed_path)):
        workbook = xlrd.open_workbook(dealed_path[i])
        #文件所包含的所有sheetname
        sheetname = workbook.sheet_names()
        conn = pymysql.connect(host='10.16.31.77', user='root', port=3306, password='AutoTest', db='chart_demo')
        cursor = conn.cursor()
        for name in sheetname:
            if len(sheetname_c) > abs(num) and name == sheetname_c[num]:
                data = pd.read_excel(dealed_path[i], sheet_name=sheetname_c[num])
                crash = int(data['value1'][0])
                print(crash)
                tstr = '2020-' + sheetname_c[num] + ' 00:00:00'
                try:
                    time.strptime(tstr, "%Y-%m-%d %H:%M:%S")
                    create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(tstr, "%Y-%m-%d %H:%M:%S")))
                except Exception:
                    # traceback.print_exc()
                    continue
                print(create_time)
                packagename = need_name[i]
                print(packagename)
                if crash == 0:
                    continue
                else:
                    sql = "insert into daily_error_detail(packagename,time,crash) values('%s','%s','%d')" % (
                    packagename, create_time, crash)
                    print(sql)
                    try:
                        cursor.execute(sql)
                        conn.commit()
                        print(sql)
                        print('~~~~~~~~~~~')

                    except:
                        conn.rollback()
                        print('-------')
            else:
                continue
        cursor.close()
        conn.close()


if __name__ == '__main__':
    find_file('./analysis_module/')
    for i in range(-3,0):
        to_error_detail('./xlsxfile/',i)


