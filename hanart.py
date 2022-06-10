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
    charset="utf8")

cursor = conn.cursor()
 
tree = ET.parse("artsmall.xml")
# 根节点
root = tree.getroot()
# 标签名
print('root_tag:',root.tag)
#artdic = {"id":"", "name":"","realname":"","profile":"","data_quality":"","images":"","namevariations":"","aliases":"","members":"","urls":""}
artlist = []
for art in root:
    print("   ",art.tag)
    artdic = {"id":"", "name":"","realname":"","profile":"","data_quality":"","images":"","namevariations":"","aliases":"","members":"","urls":""}
    for artag in art:
        #print("        ",artag.tag,":",artag.text)
        if artag.tag == 'id':
            artdic['id'] = artag.text 
        elif artag.tag == 'name':
            artdic['name'] = artag.text
        elif artag.tag == 'realname':
            artdic['realname'] = artag.text
        elif artag.tag == 'profile':
            artdic['profile'] = artag.text
        elif artag.tag == 'data_quality':
            artdic['data_quality'] = artag.text
        elif artag.tag == 'namevariations':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artdic['namevariations'] = data2
        elif artag.tag == 'aliases':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artdic['aliases'] = data2
        elif artag.tag == 'members':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artdic['members'] = data2
        elif artag.tag == 'urls':
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
            artdic['urls'] = data2
        elif artag.text is None:
            pass
 

        
        #print("        ",artag.tag,":",artag.text,",",type(artag.text))
       #  if artag.text is  None:

           # print("        ",artag.tag,":",artag.text,",",len(artag.text))
           # data2 = []
           # for arrtag in artag:
           #     data2.append(arrtag.text)
           # print("            ",arrtag.tag,":",arrtag.text)
            # print(data2)
    artlist.append(artdic) 
    #sql = 'insert into freeArtistsMeta(id,namevariations) values (%s,%s);'
    sql = 'insert into freeArtistsMeta (id, name,realname,data_quality,images,namevariations,aliases,members,urls,profile) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(sql,(artdic['id'],artdic['name'],artdic['realname'],artdic['data_quality'],artdic['images'],str(artdic['namevariations']),str(artdic['aliases']),str(artdic['members']),str(artdic['urls']),artdic['profile']))
    conn.commit()
    print(artdic)

cursor.close()
conn.close() 

#print(artlist)
