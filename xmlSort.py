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
        'keys':     ("IDHVID",),
        'values':   ("HVIDNAME",),
        'date':     "DATEEND"
    },

# SPVMPSERV 
# CODE -> N_GR
# Example:
# "09.00.15.002.331" -> "15"
    "SPVMPSERV":{
        'keys':     ("CODE",),
        'values':   ("N_GR",),
        'date':     "DEND"
    },
# SPHMET
# HVID.IDHM -> HMNAME
# Example:
# "11.00.21.006.399" -> "исправление косоглазия с пластикой экстраокулярных мышц"
# 
    "SPHMET":{
        'keys':     ("HVID", "IDHM"), 
        'values':   ("HMNAME",),
        'date':     "DATEEND"
    }
# SPMEDSERVICE
# DIVISION -> {CODE, NAME}
# Example:
# 
}

# дата окончания действия
DATE_END = "31.12.2999"

##
def getNodesFromXml(name):
    ''' str -> list of lxml.etree._Element

        Возвращает содержимое XML файла (может быть сжат в zip) в виде
        списка элементов.
    '''

    try:
        archive = zipfile.ZipFile(name + '.zip', 'r')
        f = archive.open(name + '.XML')
    except:
        f = open(name + '.XML')
        

    parser = etree.XMLParser(encoding='cp1251')
    page = etree.parse(f, parser)
    nodes = page.xpath('/ROOT/REC')

    f.close()
    return nodes

##
def readHandbook(name, nodes, fields):
    ''' (str, list, dict) -> None

        Из полученного списка \a nodes формируется словарь с именем \a name,
        в котором хранятся данные извлеченные согласно правилам заданным в
        \a fields:
        'keys' - ключевое поля (или поля, которые собираются через точку),
        'value' - значения ключей,
        'date' - проверка на актуальность даты (\a DATE_END).   
    '''
    for node in nodes:
        dateend = node.get(fields['date'])
        if dateend == DATE_END:
            key = ''

            for k in fields['keys']:
                key += node.get(k)
                key += '.'
            key = key[0:-1]
            values = {}
            for value in fields['values']:
                values[value] = node.get(value)
            globals()[name][key] = values

##
def printHandbook(name):
    ''' str -> None

        Вывод на экран справочника \a name. 
    '''
    for key in eval(name):
        print key,
        for value in eval(name)[key]:
            print eval(name)[key].get(value)

##
if __name__ == "__main__":
    for name in HANDBOOK:
        globals()[name] = {}
        nodes = getNodesFromXml(name)
        readHandbook(name, nodes, HANDBOOK[name])

    printHandbook("SPHMET")
     


      
