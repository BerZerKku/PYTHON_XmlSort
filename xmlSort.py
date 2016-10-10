# -*- coding: cp1251 -*-
from lxml import etree
import zipfile

DATE_END = "31.12.2999"

# IDHVID -> HVIDNAME   
# Example:
# "14.00.26.003" -> "Коронарная реваскуляризация миокарда с применением
# ангиопластики в сочетании со стентированием при ишемической болезни
# сердца"
SPHVID = {}

# CODE -> N_GR
# Example:
# "09.00.15.002.331" -> "15"
SPVMPSERV = {}

def readSPHVID():
    global SPHVID
    
    archive = zipfile.ZipFile('SPHVID.zip', 'r')
    f = archive.open('SPHVID.XML')

    parser = etree.XMLParser(encoding='cp1251')
    page = etree.parse(f, parser)
    nodes = page.xpath('/ROOT/REC')

    for node in nodes:
        dateend = node.get('DATEEND')
        if dateend == DATE_END:
           idhvid = node.get('IDHVID') 
           hvidname = node.get('HVIDNAME')
           SPHVID.update({idhvid: hvidname})


def readSPVMPSERV():
    global SPVMPSERV

    archive = zipfile.ZipFile('SPVMPSERV.zip', 'r')
    f = archive.open('SPVMPSERV.XML')

    parser = etree.XMLParser(encoding='cp1251')
    page = etree.parse(f, parser)
    nodes = page.xpath('/ROOT/REC')

    for node in nodes:
        dend = node.get('DEND')
        if dend == DATE_END:
           code = node.get('CODE') 
           n_gr = node.get('N_GR')
           SPVMPSERV.update({code: n_gr})
    

readSPHVID()
#for key in SPHVID:
#    print key, SPHVID.get(key)

readSPVMPSERV()
#for key in SPVMPSERV:
#    print key, SPVMPSERV.get(key)    
