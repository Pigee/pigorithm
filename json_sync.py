#!/usr/bin/env python3
import requests
import json
import urllib3
import pymysql
import time

urllib3.disable_warnings()
# get login token url
accessUrl = 'http://xxxxxxxx.com:xxxx/seeyon/rest/token'
# get data url 
dataUrl = 'http://xxxxxx.com:xxxxxx/seeyon/rest/cap4/form/soap/export'

# access info 
accessKey = {
    'userName': 'rest',
    'password': '8698238d-01db-4787-bddc-825504877ade'
}

#Mysql connection
conn = pymysql.connect(host="localhost",
                       port=3306,
                       user="xxxxxx",
                       passwd="xxxxxx",
                       db="xxxxxx")

# huatian data
_paraHt = {
    'templateCode':'KC002',
    'beginDateTime':'2020-05-10',
    'endDateTime':'2050-05-16',
    'rightId':'6485617058445084499.5105331411658818656'
}

# ziliashui data
_paraZls = {
    'templateCode':'KC001',
    'beginDateTime':'2010-05-11',
    'endDateTime':'2050-05-12',
    'rightId':'-8837841816137350410.-5843125823188152722',
}

# define header
header = {'Content-Type': 'application/json'}

############################### Handle Json Data ####################################################
def getData(paraModel,field0015):
    session = requests.session()
    response = session.post(url=accessUrl, data=json.dumps(accessKey), headers=header)

    # print(response.json()["id"])
    sign=response.json()["id"]

    # add token to header
    header['token'] = sign
    res = session.post(url=dataUrl, headers=header, data=json.dumps(paraModel))

    #jsonfile = open('jd.json', 'w', encoding='utf-8')
    #json.dump(res.json(),jsonfile,ensure_ascii=False,indent=4)
    #jsonfile.close()

    jsonData = []
    for lsdata in res.json()["data"]["data"]["data"]:
        jsonData.append((field0015,lsdata["masterData"]["field0003"]["showValue"],lsdata["masterData"]["field0004"]["showValue"],lsdata["masterData"]["field0006"]["showValue"],lsdata["masterData"]["field0009"]["showValue"],lsdata["masterData"]["field0001"]["showValue"],lsdata["masterData"]["field0002"]["showValue"],lsdata["masterData"]["field0005"]["showValue"],lsdata["masterData"]["field0007"]["showValue"],lsdata["masterData"]["field0008"]["showValue"],lsdata["masterData"]["field0014"]["showValue"],lsdata["masterData"]["field0019"]["showValue"],lsdata["masterData"]["field0018"]["showValue"],lsdata["masterData"]["field0016"]["showValue"]))

    return jsonData


##################################  Handle jj_1642732384338_sync Data ################################

def insertjsonData(jsonData):
    cursor.executemany('INSERT INTO jj_1642732384338_sync(field0015, field0003, field0004, field0006, field0009, field0001, field0002, field0005, field0007, field0008, field0014, field0019, field0018, field0016) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',jsonData);
    conn.commit()


##################################  Handle jj_1642732384338 Data #####################################
def updateData():
    cursor.execute('''update jj_1642732384338 t1 ,jj_1642732384338_sync t2
                      set t1.w_1642732438262=concat(t2.field0004,'_',t2.field0006,right(t1.w_1642732438262,12)),
                      t1.w_1642732444767=t2.field0004,
                      t1.w_1642732445083=t2.field0006,
                      t1.w_1644375318174=t2.field0009,
                      t1.w_1652424475608=t2.field0001,
                      t1.w_1652424524290=t2.field0002,
                      t1.w_1652424585213=t2.field0005,
                      t1.w_1652424622556=t2.field0007,
                      t1.w_1652424641260=t2.field0008,
                      t1.w_1652424666669=t2.field0014,
                      t1.w_1652424711872=t2.field0019,
                      t1.w_1652424727668=t2.field0018,
                      t1.w_1652424740567=t2.field0016
                     where t1.w_1642732440485 = t2.field0015 and t1.w_1642732444424 = t2.field0003''')
    conn.commit()


def insertData():
    cursor.execute('''INSERT INTO jj_1642732384338(id, create_user_id, create_user, create_date, update_user_id, update_user, 
                      update_date, w_1642732438262, w_1642732440485, w_1642732444424, w_1642732444767, w_1642732445083, w_1644375318174,
                      w_1652424475608, w_1652424524290, w_1652424585213, w_1652424622556, w_1652424641260, w_1652424666669, w_1652424711872,
                      w_1652424727668, w_1652424740567, w_1652424757817) 
                      select replace(uuid(),'-',''), 'jj', '晋江自来水有限公司',now(), 'jj', '晋江自来水有限公司',now(),
                      concat(t2.field0004,'_',t2.field0006,'_',date_format(now(),'%Y%m'),'_0',left(rand()*100000,3)), 
                      t2.field0015, t2.field0003, t2.field0004, t2.field0006, t2.field0009, t2.field0001, t2.field0002, t2.field0005,
                      t2.field0007, t2.field0008, t2.field0014, t2.field0019, t2.field0018, t2.field0016, t2.field0017
                      from jj_1642732384338_sync t2 left join jj_1642732384338 t1 on t1.w_1642732440485 = t2.field0015 and t1.w_1642732444424 = t2.field0003
                      where t1.w_1642732440485 is null''')
    conn.commit()

def deleteData():
    cursor.execute('''with temp as (
                      select  t2.w_1642732440485,t2.w_1642732444424,t1.field0015 from jj_1642732384338 t2 
                      left join jj_1642732384338_sync t1 on t2.w_1642732440485 = t1.field0015 and t2.w_1642732444424 = t1.field0003 
                      where t1.field0015 is null)
                      delete from jj_1642732384338 where concat(w_1642732440485,w_1642732444424) in 
                      (select concat(w_1642732440485,w_1642732444424) from temp)''')
    conn.commit()

def createTable():
    cursor.execute('''CREATE TABLE jj_1642732384338_sync (
                      field0015 varchar(100) NOT NULL DEFAULT '',
                      field0003 varchar(100) NOT NULL DEFAULT '',
                      field0004 varchar(100) NOT NULL DEFAULT '',
                      field0006 varchar(100) NOT NULL DEFAULT '',
                      field0009 varchar(100) NOT NULL DEFAULT '',
                      field0001 varchar(100) NOT NULL DEFAULT '',
                      field0002 varchar(100) NOT NULL DEFAULT '',
                      field0005 varchar(100) NOT NULL DEFAULT '',
                      field0007 varchar(100) NOT NULL DEFAULT '',
                      field0008 varchar(100) NOT NULL DEFAULT '',
                      field0014 varchar(100) NOT NULL DEFAULT '',
                      field0019 varchar(100) NOT NULL DEFAULT '',
                      field0018 varchar(100) NOT NULL DEFAULT '',
                      field0016 varchar(100) NOT NULL DEFAULT '',
                      field0017 varchar(100) NOT NULL DEFAULT ''
                      )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ''');
    conn.commit()
  
# comment the unnecessary function if you do not need it 
def mainLogic():
    # create cusor and clear his data of jj_1642732384338_sync
    # cursor = conn.cursor()
    createTable()
    cursor.execute('truncate table jj_1642732384338_sync')

    # get 华天 data and insert into jj_1642732384338_sync
    htdata=getData(_paraHt,'xxxxxx')
    insertjsonData(htdata)

    # get 自来水 data  and insert into  jj_1642732384338_sync

    zlsdata=getData(_paraZls,'xxxxx')
    insertjsonData(zlsdata)

    # update data from  jj_1642732384338_sync to jj_1642732384338
    #updateData()

    # insert data from  jj_1642732384338_sync to jj_1642732384338
    #insertData()

   # delete from  jj_1642732384338
    #deleteData()

    #cursor.close()
    #conn.close()


####################################### Main logic porter ###########################################
if __name__ == '__main__':

    cursor = conn.cursor()
    while True:
        mainLogic()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),':main logic finished, sleeping 600 sec....')
        time.sleep(600)

    cursor.close()
    conn.close()

