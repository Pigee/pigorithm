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

infile = r'rel.xml'

# declare all variable
rellist = [0,'','','','','','','','','']
artists_tag = False
lablist = []
genlist = []
stylist = []

insertlist = []

y = 2000 # row number for each inserts
# instr = "insert into freeRelease values "

# print(instr)


#context = etree.iterparse(infile,events=("start", "end"))
# for event, element in context:
for event, element in etree.iterparse(infile,events=("start", "end"),encoding='UTF-8'):
    if event == "start" and element.tag == "release":
        rellist[0] = element.get("id")
        # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 
    elif event == "start" and element.tag == "notes" and element.text is not None:
        rellist[1] = element.text
    elif event == "start" and element.tag == "format":
        rellist[2] = element.get("name")
    elif event == "start" and element.tag == "artists": #set tag to  
        artists_tag = True 
    elif event == "start" and element.tag == "id" and artists_tag and element.text is not None:
        rellist[4] = element.text
        artists_tag = False 
    elif event == "start" and element.tag == "label":
        lablist.append(element.get("id"))
        rellist[5] = str(lablist)
    elif event == "start" and element.tag == "genre":
        genlist.append(element.text)
        rellist[6] = str(genlist)
    elif event == "start" and element.tag == "style":
        stylist.append(element.text)
        rellist[7] = str(stylist)
    elif event == "start" and element.tag == "released" and element.text is not None:
        rellist[8] = element.text
    elif event == "start" and element.tag == "country" and element.text is not None:
        rellist[9] = element.text

    elif event == "end" and element.tag == "release":
      
        # print(rellist[0])
        if int(rellist[0]) < y:
            insertlist.append(rellist)
        else:
            cursor.executemany('insert into freeRelease (id, notes,formats,images,artists, labels,genres,styles,released,country) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',insertlist)
            conn.commit()
            print(time.strftime("%Y-%m-%d %X", time.localtime()),':Handle to ',rellist[0],'records...')
            y += 2000
            insertlist = []



        #reset all temporary variab
        rellist = [0,'','','','','','','','','']
        lablist = []
        genlist = []
        stylist = []


    # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 

    # release the memory so that your computer won`t collapse...
    element.clear() 

