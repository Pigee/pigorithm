#!/usr/bin/env python3

'''
parse xml data and insert into mysql
http://data.discogs.com/?prefix=data/2022/
 freeArtistsMeta (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls)
 freeMasters (id, main_release,videos,images,artists, data_quality,genres,styles,year,title)
 freeRelease (id, notes,formats,images,artists, labels,genres,styles,released,country)
'''

from lxml import etree

infile = r'relsmall.xml'

# declare all variable
artdic = {"id":"", "notes":"","formats":"","images":"","artists":"","labels":"","genres":"","styles":"","released":"","country":""}
artists_tag = False
lablist = []
genlist = []
stylist = []
i = 0
instr = "insert into freeRelease values "

print(instr)


#context = etree.iterparse(infile,events=("start", "end"))
# for event, element in context:
for event, element in etree.iterparse(infile,events=("start", "end"),encoding='UTF-8'):
    if event == "start" and element.tag == "release":
        artdic['id'] = element.get("id")
        # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 
    elif event == "start" and element.tag == "notes":
        artdic['notes'] = element.text
    elif event == "start" and element.tag == "format":
        artdic['formats'] = element.get("name")
    elif event == "start" and element.tag == "artists": # 
        artists_tag = True 
    elif event == "start" and element.tag == "id" and artists_tag:
        artdic['artists'] = element.text
        artists_tag = False 
    elif event == "start" and element.tag == "label":
        lablist.append(element.get("id"))
        artdic['labels'] = str(lablist)
    elif event == "start" and element.tag == "genre":
        genlist.append(element.text)
        artdic['genres'] = str(genlist)
    elif event == "start" and element.tag == "style":
        stylist.append(element.text)
        artdic['styles'] = str(stylist)
    elif event == "start" and element.tag == "released":
        artdic['released'] = element.text
    elif event == "start" and element.tag == "country":
        artdic['country'] = element.text

    elif event == "end" and element.tag == "release":
        print(artdic)
        dicstr =  "(" + artdic['id'] + ",'" + artdic['notes'] + "','"+ artdic['formats'] + "','"  + artdic['artists'] + "','" + artdic['labels']  + "','" + artdic['genres'] + "','" + artdic['styles'] + "','" + artdic['released'] + "','" + artdic['country'] + "')" 
        

        #reset all temporary variable
        artdic = {"id":"", "notes":"","formats":"","images":"","artists":"","labels":"","genres":"","styles":"","released":"","country":""}
        lablist = []
        genlist = []
        stylist = []
        
        print(dicstr)

    # print("%5s, %4s, %s, %s" % (event, element.tag, element.get("id"), element.text)) 

    # release the memory so that your computer won`t collapse...
    element.clear() 

