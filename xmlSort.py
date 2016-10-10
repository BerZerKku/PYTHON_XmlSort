# -*- coding: cp1251 -*-
from lxml import etree
import zipfile

HANDBOOK = {
# SPHVID
# IDHVID -> HVIDNAME   
# Example:
# "14.00.26.003" -> "Коронарная реваскуляризация миокарда с применением
# ангиопластики в сочетании со стентированием при ишемической болезни
# сердца"
    "SPHVID":{
        'keys':  ("IDHVID",),
        'value': "HVIDNAME",
        'date':  "DATEEND"
    },

# SPVMPSERV 
# CODE -> N_GR
# Example:
# "09.00.15.002.331" -> "15"
    "SPVMPSERV":{
        'keys':  ("CODE",),
        'value': "N_GR",
        'date':  "DEND"
    },
# SPHMET
# HVID.IDHM -> HMNAME
# Example:
# "11.00.21.006.399" -> "исправление косоглазия с пластикой экстраокулярных мышц"
# 
    "SPHMET":{
        'keys':  ("HVID", "IDHM"), 
        'value': "HMNAME",
        'date':  "DATEEND"
    }
}

# дата окончания действия
DATE_END = "31.12.2999"


def readHandbook(name, fields):
    ''' (str, dict) -> None

        Считывается из заархивированного файла \a name ".zip" одноименного файла
        ".xml". Затем формируется словарь с тем же именем, в котором хранятся
        данные извлеченные согласно правилам заданным в \a fields:
        'keys' - ключевое поля (или поля, которые собираются через точку),
        'value' - значение ключев,
        'date' - проверка на актуальность даты (\a DATE_END).   
    '''
    
    archive = zipfile.ZipFile(name + '.zip', 'r')
    f = archive.open(name + '.XML')

    parser = etree.XMLParser(encoding='cp1251')
    page = etree.parse(f, parser)
    nodes = page.xpath('/ROOT/REC')

    for node in nodes:
        dateend = node.get(fields['date'])
        if dateend == DATE_END:
            key = ''

            for k in fields['keys']:
                key += node.get(k)
                key += '.'
            key = key[0:-1]
            value = node.get(fields['value'])
            globals()[name][key] = value


for name in HANDBOOK:
    globals()[name] = {}
    readHandbook(name, HANDBOOK[name])          

#for key in SPHMET:
#    print key, SPHMET.get(key)   
