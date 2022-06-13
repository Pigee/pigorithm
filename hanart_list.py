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

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sa",
    database="upwork",
    charset="utf8mb4")

cursor = conn.cursor()
 
tree = ET.parse("art.xml")
# 根节点
root = tree.getroot()
# 标签名
print('root_tag:',root.tag)
#artlist = {"id":"", "name":"","realname":"","profile":"","data_quality":"","images":"","namevariations":"","aliases":"","members":"","urls":""}
insertlist = []
y = 2000

for art in root:
    print("   ",art.tag)
    #artlist = {"id":"", "name":"","realname":"","profile":"","data_quality":"","images":"","namevariations":"","aliases":"","members":"","urls":""}
    artlist = ['','','','','','','','','','']

    for artag in art:
        #print("        ",artag.tag,":",artag.text)
        if artag.tag == 'id':
            artlist[0] = artag.text 
        elif artag.tag == 'name':
            artlist[1] = artag.text
        elif artag.tag == 'realname':
            artlist[2] = artag.text
        elif artag.tag == 'profile':
            artlist[3] = artag.text
        elif artag.tag == 'data_quality':
            artlist[4] = artag.text
        elif artag.tag == 'namevariations':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artlist[6] = str(data2)
        elif artag.tag == 'aliases':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artlist[7] = str(data2)
        elif artag.tag == 'members':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artlist[8] = str(data2)
        elif artag.tag == 'urls':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artlist[9] = data2
 
    if int(artlist[0]) < y:
        insertlist.append(rellist)
    else:
        cursor.executemany('insert into freeart (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',insertlist)
        conn.commit()
        print(time.strftime("%Y-%m-%d %X", time.localtime()),':Handle to ',artlist[0],'records...')
        y += 2000
        insertlist = []

    #print(artlist)

cursor.close()
conn.close() 

#print(artlist)
