# -*- coding: cp1251 -*-
from lxml import etree
import zipfile

# IDHVID -> VIDNAME   
# Example:
# "14.00.26.003" -> "Коронарная реваскуляризация миокарда с применением
# ангиопластики в сочетании со стентированием при ишемической болезни
# сердца"
SPHVID = {} 

def readSPHVID():
    global SPHVID
    
    archive = zipfile.ZipFile('SPHVID.zip', 'r')
    f = archive.open('SPHVID.XML')

    parser = etree.XMLParser(encoding='cp1251')
    page = etree.parse(f, parser)
    nodes = page.xpath('/ROOT/REC')

    for node in nodes:
        DATEEND = node.get('DATEEND')
        if DATEEND == "31.12.2999":
           IDHVID = node.get('IDHVID') 
           VIDNAME = node.get('HVIDNAME')
           SPHVID.update({IDHVID: VIDNAME})
    
    for key in SPHVID:
        print key, SPHVID.get(key)




readSPHVID()
