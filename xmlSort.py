# -*- coding: cp1251 -*-
from lxml import etree
import zipfile

# дата окончания действия
DATE_END = "31.12.2999"

# необходимые отделения
DIVISION = ("106", "156")

HANDBOOK = {
# SPHVID
# IDHVID -> HVIDNAME   
# Example:
# "14.00.26.003" -> {IDHVID="Коронарная реваскуляризация миокарда с применением
# ангиопластики в сочетании со стентированием при ишемической болезни
# сердца"}
    "SPHVID":{
        'keys':     "IDHVID",
        'values':   ("HVIDNAME",),
        'date':     "DATEEND"
    },

# SPVMPSERV 
# CODE -> N_GR
# Example:
# "09.00.15.002.331" -> "15"
    "SPVMPSERV":{
        'keys':     "CODE",
        'values':   ("N_GR",),
        'date':     "DEND"
    },
# SPHMET
# HVID + '.' + IDHM -> HMNAME
# Example:
# "11.00.21.006.399" -> {"N_GR" = "исправление косоглазия с пластикой
# экстраокулярных мышц"}
    "SPHMET":{
        'keys':     ("HVID", "IDHM"), 
        'values':   ("HMNAME",),
        'date':     "DATEEND"
    },
# SPMEDSERVICE
# DIVISION -> {CODE, NAME}
# Example:
# "106" -> {CODE="10.00.19.004.371",NAME="операции по реиннервации и заместительной
# функциональной пластике гортани и трахеи с применением микрохирургической техники
# и электромиографическим мониторингом;Реконструктивно-пластическое восстановление
# функции гортани и трахеи"}
    "SPMEDSERVICE":{
        'keys':     "CODE",
        'values':   ("DIVISION", "NAME"),
        'date':     "DEND"
    }
}

# Внешние справочники
SPHVID = {}
SPHMET = {}
SPHMET = {}
SPMEDSERVICE = {}
# Сформированные справочники
GLB_HANDBOOK = {}

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
    print "Cправочник %s." % (name),
    for node in nodes:
        dateend = node.get(fields['date'])
        if dateend != DATE_END:
            continue
        
        division = node.get('DIVISION')
        if division is not None:
            if not (division in DIVISION):
                continue
            
        key = ''
        if type(fields['keys']) == str:
            key = node.get(fields['keys'])
        else :
            for k in fields['keys']:
                key += node.get(k)
                key += '.'
            key = key[0:-1]
        values = {}
        for value in fields['values']:
            values[value] = node.get(value)
        globals()[name].update({key: values})

    l1 = len(globals()[name])
    l2 = len(nodes)
    print "Считано %s из %s." % (l1, l2)


##
def printHandbook(name):
    ''' str -> None

        Вывод на экран справочника \a name. 
    '''
    for key in eval(name):
        print key,
        for value in eval(name)[key]:
            print "value = ", eval(name)[key].get(value),
            print


##
def createHandbook():
    global GLB_HANDBOOK
    ''' (None) -> None

        Формирование конечного словаря:
        CODE -> dict{DIVISION, NAME, HVIDNAME, HMNAME, N_GR}
    '''

    for code in SPMEDSERVICE:
        data = {}
        name = SPMEDSERVICE[code].get("NAME")
        data["NAME"] = name;

        hmname = 'None'
        if code in SPHMET:
            hmname = SPHMET[code].get("HMNAME")
        data["HMNAME"] = hmname;

        #pos = code.rfind('.')
        idhvid = code[0:code.rfind('.')] 
        hvidname = 'None'
        if code[0:code.rfind('.')] in SPHVID:
            hvidname = SPHVID[idhvid].get("HVIDNAME")
        data["HVIDNAME"] = hvidname
        
        n_gr = 'None'
        if code in SPVMPSERV:
            n_gr = SPVMPSERV[code].get("N_GR")
        data["N_GR"] = n_gr
        GLB_HANDBOOK.update({code: data})
            

def saveFile(name):
    f = open(name, "w")

    cnt = 0
    for code in GLB_HANDBOOK:
        cnt += 1
        if cnt >= 100:
            break;
        name = GLB_HANDBOOK[code].get("NAME")
        hmname = GLB_HANDBOOK[code].get("HMNAME")
        hvidname = GLB_HANDBOOK[code].get("HVIDNAME")
        n_gr = GLB_HANDBOOK[code].get("N_GR")
        s = code + ',' + name + ',' + hmname + ',' + hvidname + ',' + n_gr + '\n'
        f.write(s.encode("cp1251"))
        
    f.close()
    


##
if __name__ == "__main__":
    for name in HANDBOOK:
        globals()[name] = {}
        nodes = getNodesFromXml(name)
        readHandbook(name, nodes, HANDBOOK[name])
    
    #printHandbook("SPVMPSERV")

    createHandbook()

    saveFile(u"file.txt")
     


      
