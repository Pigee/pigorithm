#!/usr/bin/python3

import pymysql
import datetime

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='sxadmin',
                     password='sx@123',
                     database='sxdbman')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 随机获得一条客户信息
def getzh(jl):
    sql = " SELECT ye,khsj,id from zhxx where khsj < %s and ye > 0 order by rand() limit 1 "
    cursor.execute(sql,(jl[1]))
    results = cursor.fetchone()
    return results

#  Check whether the record is suitable for the user
def shoot(jl,zh):
    zhtime = datetime.datetime.strptime(zh[1],'%Y-%m-%d %H:%M:%S')
    if (jl[0] <= zh[0] and jl[1] > zhtime):
        return True
    else:
        return False

def updatezh(jl,zh):
    row2 = cursor.execute("update zhxx set ye = %s - %s where id = %s", (zh[0],jl[0],zh[2]))
    db.commit()

def updatejl(jl,zh):
    row2 = cursor.execute("update zhjl set id =  %s ,ye = %s - %s where jlid = %s", (zh[2],zh[0],jl[0],jl[2]))
    db.commit()

def updatezh_gt(jl,zh):
    row2 = cursor.execute("update zhxx set ye = 0 where id = %s", (zh[2]))
    db.commit()

def updatejl_gt(jl,zh):
    row = cursor.execute("update zhjl set id =  %s ,ck = %s ,ye = 0 where jlid = %s", (zh[2],zh[0],jl[2]))
    row2 = cursor.execute("insert into zhjl(ck,cktime) values (%s,%s)", ((jl[0]-zh[0]),jl[1]))
    db.commit()



# Main logic  
def getjl():
    sql = """ SELECT ck,cktime,jlid from zhjl where ye is null order by cktime desc """
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        zh = getzh(row)  
        if row[0] <= zh[0] :
            updatezh(row,zh)
            updatejl(row,zh)
            print("update zhjl ID:", row[2])
        else :
            updatezh_gt(row,zh)
            updatejl_gt(row,zh)
            print("update and insert zhjl ID:", row[2])

getjl()
# getzh()

# 关闭数据库连接
db.close()


