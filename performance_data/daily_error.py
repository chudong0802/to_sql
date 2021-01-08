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


def need_data(path,num):
    workbook_c = xlrd.open_workbook(path+'com.hryt.desktop.xlsx')
    sheetname_c = workbook_c.sheet_names()
    # print(sheetname_c)
    dealed_path = []#删选出来文件的所有路径
    for needed_name in os.listdir(path):
        needed_file = os.path.join(path,needed_name)
        dealed_path.append(needed_file)
    crash_all = []
    for i in range(0,len(dealed_path)):
        workbook = xlrd.open_workbook(dealed_path[i])
        #文件所包含的所有sheetname
        sheetname = workbook.sheet_names()
        for name in sheetname:
            if name == sheetname_c[num]:
                # for j in range(1,len(need_date)):
                data = pd.read_excel(dealed_path[i], sheet_name=sheetname_c[num])
                crash = int(data['value1'][0])
                print(crash)
                crash_all.append(crash)
            else:
                continue
    print(crash_all)
    need_crash = np.sum(crash_all, axis=0)
    print(need_crash)
    tstr = '2020-'+ sheetname_c[num]+' 00:00:00'
    time.strptime(tstr, "%Y-%m-%d %H:%M:%S")
    create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(tstr, "%Y-%m-%d %H:%M:%S")))
    print(create_time)

    conn = pymysql.connect(host='10.16.31.77', user='root', password='AutoTest', port=3306, db='chart_demo')
    cursor = conn.cursor()
    sql = "insert into daily_error(time,crash) values('%s','%d')" % (create_time, need_crash)
    print(sql)
    try:
        # values = (dalvik_max,dalvik_min,dalvik_avg,native_max,native_min,native_avg,cpu_max,cpu_min,cpu_avg,crash)
        cursor.execute(sql)
        conn.commit()
        print('....................')
    except:
        conn.rollback()
        print(sql)
        print('=====================')
    
    cursor.close()
    conn.close()

if __name__ == '__main__':
    find_file('./analysis_module/')
    for num in range(-3,0):
        need_data('./xlsxfile/',num)


