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
# import pymysql

'''
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="sa",
    database="upwork",
    charset="utf8mb4")

cursor = conn.cursor()
'''

infile = r'lab.xml'

# declare all variable
rellist = ['','','','','','','','',]

lab_tag = True
Reset_tag = False

urllist = []
lablist = []

insertlist = []

y = 2000 # row number for each inserts

# create table freeLabel (id int, name varchar(1000),contactinfo varchar(2000), profile varchar(2000),data_quality varchar(200),images varchar(20),urls varchar(4000),sublabels varchar(2000))
# freeLabel (id, name,contactinfo, profile,data_quality,images,urls,sublabels)
#context = etree.iterparse(infile,events=("start", "end"))
# for event, element in context:
for event, element in etree.iterparse(infile,events=("start", "end"),encoding='UTF-8'):
    if event == "start" and element.tag == "id":
        rellist[0] = element.text
        # max(insertlist)[0]
        # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 
    elif event == "start" and element.tag == "name" and element.text is not None:
        rellist[1] = element.text
    elif event == "start" and element.tag == "contactinfo" and element.text is not None:
        rellist[2] = element.text
    elif event == "start" and element.tag == "profile" and element.text is not None:
        rellist[3] = element.text
    elif event == "start" and element.tag == "data_quality" and element.text is not None:
        rellist[4] = element.text

    elif event == "start" and element.tag == "url" and element.text is not None:
        urllist.append(element.text)
        rellist[6] = str(urllist)

    elif event == "start" and element.tag == "sublabels": #set tag to  
        lab_tag = True 
        reset_tag = False
    elif event == "start" and element.tag == "label" and lab_tag:
        lablist.append(element.get("id"))
        rellist[7] = str(lablist)
    elif event == "end" and element.tag == "sublabels": #set tag to  
        lab_tag = False 
        reset_tag = True

    elif event == "end" and element.tag == "label" and reset_tag:
      
        print(rellist[0])
        if int(rellist[0]) < y:
            insertlist.append(rellist)
        else:
            #cursor.executemany('insert into freeMasters (id, main_release,videos,images,artists, data_quality,genres,styles,year,title) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',insertlist)
            #conn.commit()
            #print(time.strftime("%Y-%m-%d %X", time.localtime()),':Handle to ',rellist[0],'records...')
            y += 2000
            insertlist = []



        #reset all temporary variab
        rellist = ['','','','','','','','']
        lablist = []
        urllist = []


    # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 

    # release the memory so that your computer won`t collapse...
    element.clear() 

