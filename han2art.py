#!/usr/bin/env python3
'''
遇到问题没人解答？小编创建了一个Python学习交流QQ群：531509025
寻找有志同道合的小伙伴，互帮互助,群里还有不错的视频学习教程和PDF电子书！
'''
import xml.sax
 
class StudentHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.namevariations = ""
 
    # 元素开始调用
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "artist":
            pass
 
    # 元素结束调用
    def endElement(self, tag):
        if self.CurrentData == "id":
            print("id:", self.id)
        elif self.CurrentData == "name":
            print("name:", self.name)
        elif self.CurrentData == "namevariations":
            print("namevariations:", self.namevariations.name)

        self.CurrentData = ""
 
    # 读取字符时调用
    def characters(self, content):
        if self.CurrentData == "id":
            self.id = content
        elif self.CurrentData == "name":
            self.name = content
        elif self.CurrentData == "namevariations":
            self.name = content

if (__name__ == "__main__"):
    # 创建 XMLReader
    parser = xml.sax.make_parser()
    # 关闭命名空间
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # 重写 ContextHandler
    Handler = StudentHandler()
    parser.setContentHandler(Handler)
    parser.parse("artsmall.xml")

