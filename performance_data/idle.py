import  pandas as pd
import json
import pymysql
import datetime,time
import os
import xlrd

def to_summary(path):
    workbook = xlrd.open_workbook(path)
    # 文件所包含的所有sheetname
    sheetname = workbook.sheet_names()
    print(sheetname)

    conn = pymysql.connect(host='10.16.31.77', user='root', password='AutoTest', port=3306,database='chart_demo')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    for i in range(-3,0):
        data = pd.read_excel(path,sheet_name=sheetname[i])
        df = pd.DataFrame(data)
        for k in range(len(df['TIME'])):

            tstr = '2020-'+sheetname[i]+' ' + str(data['TIME'][k])
            try:
                time.strptime(tstr, "%Y-%m-%d %H:%M:%S")
                create_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(tstr, "%Y-%m-%d %H:%M:%S")))
            except Exception:
                # traceback.print_exc()
                continue
            print(create_time)

            idle = int(300 - df['%idle'][k])

            sql = "insert into idle (idle,time) values('%d','%s')"%(idle,create_time)
            print(sql)
            try:
                cursor.execute(sql)
                conn.commit()
                print(".......")
            except:
                conn.rollback()
                print("======")

    cursor.close()
    conn.close()

        
if __name__ == '__main__':
    to_summary('./analysis_module/aasummary.xlsx')