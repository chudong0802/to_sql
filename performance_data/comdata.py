import  pandas as pd
import json
import pymysql
import datetime,time
import os
import xlrd
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


def to_com_data(path,num):
    workbook_c = xlrd.open_workbook(path+'com.hryt.desktop.xlsx')
    sheetname_c = workbook_c.sheet_names()
    # print(sheetname_c)

    dealed_path = []#删选出来文件的所有路径
    tablename = []
    for needed_name in os.listdir(path):
        tablename.append(needed_name.split('.xlsx')[0])
        needed_file = os.path.join(path,needed_name)
        dealed_path.append(needed_file)
    for i in range(len(dealed_path)):
        workbook = xlrd.open_workbook(dealed_path[i])
        # 文件所包含的所有sheetname
        sheetname = workbook.sheet_names()
        for name in sheetname:

            if len(sheetname_c) > abs(num) and name == sheetname_c[num]:
                data = pd.read_excel(dealed_path[i], sheet_name=sheetname_c[num])
                # print(data)
                crash = int(data['value1'][0])
                dalvik_max = int(data['value2'][0])
                dalvik_min = int(data['value2'][1])
                dalvik_avg = int(data['value2'][2])
                native_max = int(data['value2'][3])
                native_min = int(data['value2'][4])
                native_avg = int(data['value2'][5])
                cpu_max = int(data['value2'][6])
                cpu_min = int(data['value2'][7])
                cpu_avg = int(data['value2'][8])

                tstr = '2020-' + sheetname_c[num] + ' 00:00:00'
                try:
                    time.strptime(tstr, "%Y-%m-%d %H:%M:%S")
                    create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(tstr, "%Y-%m-%d %H:%M:%S")))
                except Exception:
                    # traceback.print_exc()
                    continue
                # print(create_time)
                # 写入数据库
                conn = pymysql.connect(host='10.16.31.77', user='root', password='AutoTest', port=3306,
                                       db='chart_demo')
                cursor = conn.cursor()
                sql = "insert into chart_demo.`%s` " \
                      "(dalvik_max,dalvik_min,dalvik_avg,native_max,native_min,native_avg,cpu_max,cpu_min,cpu_avg,crash,time) " \
                      "values('%d','%d','%d','%d','%d','%d','%d','%d','%d','%d','%s')" \
                      % (tablename[i], dalvik_max, dalvik_min, dalvik_avg, native_max, native_min, native_avg, cpu_max, cpu_min,
                         cpu_avg, crash, create_time)
                # print(sql)
                try:
                    # values = (dalvik_max,dalvik_min,dalvik_avg,native_max,native_min,native_avg,cpu_max,cpu_min,cpu_avg,crash)
                    cursor.execute(sql)
                    conn.commit()
                    print(sql)
                    print('....................')
                except:
                    conn.rollback()
                    print('=====================')
                cursor.close()
                conn.close()
            else:
                continue


if __name__ == '__main__':
    find_file('./analysis_module/')
    for i in range(-3,0):
        to_com_data('./xlsxfile/',i)


