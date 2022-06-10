#!/usr/bin/env python3
'''
parse xml data and insert into mysql
http://data.discogs.com/?prefix=data/2022/
 freeArtistsMeta (id, name,realname, profile,data_quality,images,namevariations,aliases,members,urls)
 freeMasters (id, main_release,videos,images,artists, data_quality,genres,styles,year,title)
 freeRelease (id, notes,formats,images,artists, labels,genres,styles,released,country)
'''
import xml.etree.ElementTree as ET
 
tree = ET.parse("artsmall.xml")
# 根节点
root = tree.getroot()
# 标签名
print('root_tag:',root.tag)
#artdic = {"id":"", "name":"","realname":"","profile":"","data_quality":"","images":"","namevariations":"","aliases":"","members":"","urls":""}
artlist = []
for art in root:
    print("   ",art.tag)
    # artdata = []
    
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
            artdic['pfofile'] = artag.text
        elif artag.tag == 'data_quality':
            artdic['data_quality'] = artag.text

        
        #print("        ",artag.tag,":",artag.text,",",type(artag.text))
        if artag.text is not None:
            print("        ",artag.tag,":",artag.text,",",len(artag.text))
            data2 = []
            for arrtag in artag:
                data2.append(arrtag.text)
           # print("            ",arrtag.tag,":",arrtag.text)
            print(data2)
    artlist.append(artdic) 
    #print(artdic)

print(artlist)
