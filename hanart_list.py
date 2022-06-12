#!/usr/bin/env python3

'''
parse xml data and insert into mysql
http://data.discogs.com/?prefix=data/2022/
 freeArtistsMeta (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls)
 freeMasters (id, main_release,videos,images,artists, data_quality,genres,styles,year,title)
 freeRelease (id, notes,formats,images,artists, labels,genres,styles,released,country)
'''

import time
from lxml import etree
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sa",
    database="upwork",
    charset="utf8mb4")

cursor = conn.cursor()

infile = r'art.xml'

# declare all variable
rellist = [0,'','','','','','','','','']

id_tag = True
name_tag = True
var_tag = False
ali_tag = False
mem_tag = False

varlist = []
alilist = []
memlist = []
urllist = []

insertlist = []

y = 2000 # row number for each inserts

#freeArtistsMeta (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls)
#context = etree.iterparse(infile,events=("start", "end"))
# for event, element in context:
for event, element in etree.iterparse(infile,events=("start", "end"),encoding='UTF-8'):
    if event == "start" and element.tag == "id" and id_tag and element.text is not None:
        rellist[0] = element.text
        id_tag = False
        # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 
    elif event == "start" and element.tag == "name" and name_tag and element.text is not None:
        rellist[1] = element.text
        name_tag = False
    elif event == "start" and element.tag == "realname" and element.text is not None:
        rellist[2] = element.text
    elif event == "start" and element.tag == "profile" and element.text is not None:
        rellist[3] = element.text
    elif event == "start" and element.tag == "data_quality" and element.text is not None:
        rellist[4] = element.text

    elif event == "start" and element.tag == "namevariations": #set tag to  
        var_tag = True 
    elif event == "start" and element.tag == "name" and var_tag and element.text is not None:
        varlist.append(element.text)
        rellist[6] = str(varlist)
    elif event == "end" and element.tag == "namevariations": #set tag to  
        var_tag = False

    elif event == "start" and element.tag == "aliases": #set tag to  
        ali_tag = True 
    elif event == "start" and element.tag == "name" and ali_tag and element.text is not None:
        alilist.append(element.text)
        rellist[7] = str(alilist)
    elif event == "end" and element.tag == "aliases": #set tag to  
        ali_tag = False

    elif event == "start" and element.tag == "members": #set tag to  
        mem_tag = True 
    elif event == "start" and element.tag == "name" and mem_tag and element.text is not None:
        memlist.append(element.text)
        rellist[8] = str(memlist)
    elif event == "end" and element.tag == "members": #set tag to  
        mem_tag = False


    elif event == "start" and element.tag == "url":
        urllist.append(element.text)
        rellist[9] = str(urllist)

    elif event == "end" and element.tag == "artist":
             
        # print(rellist)

        if int(rellist[0]) < y:
            insertlist.append(rellist)
        else:
            cursor.executemany('insert into freeart (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',insertlist)
            conn.commit()
            print(time.strftime("%Y-%m-%d %X", time.localtime()),':Handle to ',rellist[0],'records...')
            y += 2000
            insertlist = []

        #reset all temporary variab
        rellist = [0,'','','','','','','','','']
        varlist = []
        alilist = []
        memlist = []
        urllist = []
        id_tag = True
        name_tag = True



    # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 

    # release the memory so that your computer won`t collapse...
    element.clear() 

