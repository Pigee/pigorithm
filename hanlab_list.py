#!/usr/bin/env python3
'''
parse xml data and insert into mysql
http://data.discogs.com/?prefix=data/2022/
 freeArtistsMeta (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls)
 freeMasters (id, main_release,videos,images,artists, data_quality,genres,styles,year,title)
 freeRelease (id, notes,formats,images,artists, labels,genres,styles,released,country)
'''
import xml.etree.ElementTree as ET
import pymysql
import time

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sa",
    database="upwork",
    charset="utf8mb4")

cursor = conn.cursor()
 
tree = ET.parse("lab.xml")
# 根节点
root = tree.getroot()
# 标签名
print('root_tag:',root.tag)
#labdic = {"id":"", "name":"","realname":"","profile":"","data_quality":"","images":"","namevariations":"","aliases":"","members":"","urls":""}
# create table freeLabel (id int, name varchar(1000),contactinfo varchar(2000), profile varchar(2000),data_quality varchar(200),images varchar(20),urls varchar(4000),sublabels varchar(2000))
# freeLabel (id, name,contactinfo, profile,data_quality,images,urls,sublabels)
# artlist = []
y = 2000
insertlist = []
for art in root:
    #print("   ",art.tag)
    labdic = ['','','','','','','','']
    for artag in art:
        # print("        ",artag.tag)
        if artag.tag == 'id':
            #print(artag.text)
            labdic[0] = artag.text 
        elif artag.tag == 'name' and artag.text is not None:
            labdic[1] = artag.text
        elif artag.tag == 'contactinfo' and artag.text is not None:
            labdic[2] = artag.text
        elif artag.tag == 'profile' and artag.text is not None:
            labdic[3] = artag.text
        elif artag.tag == 'data_quality' and artag.text is not None:
            labdic[4] = artag.text
        elif artag.tag == 'urls':
            urllist = []
            for arrtag in artag:
                urllist.append(arrtag.text)
            labdic[6] = str(urllist)
        elif artag.tag == 'sublabels':
            lablist = []
            for arrtag in artag:
                lablist.append(arrtag.get("id"))
            labdic[7] = str(lablist)

    if int(labdic[0]) < y:
        insertlist.append(labdic) 
    else:
        cursor.executemany('insert into freeLabel (id, name,contactinfo, profile,data_quality,images,urls,sublabels) values (%s,%s,%s,%s,%s,%s,%s,%s)',insertlist)
        conn.commit()
        print(time.strftime("%Y-%m-%d %X", time.localtime()),':Handle to ',labdic[0],'records...')
        y += 2000
        insertlist = []

    #print(labdic)
cursor.close()
conn.close() 

#print(artlist)
