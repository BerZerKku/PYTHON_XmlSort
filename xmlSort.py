# -*- coding: cp1251 -*-
from lxml import etree
import zipfile

HANDBOOK = {
# SPHVID
# IDHVID -> HVIDNAME   
# Example:
# "14.00.26.003" -> "���������� ���������������� �������� � �����������
# ������������� � ��������� �� �������������� ��� ����������� �������
# ������"
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
# "11.00.21.006.399" -> "����������� ���������� � ��������� ��������������� ����"
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

# ���� ��������� ��������
DATE_END = "31.12.2999"

##
def getNodesFromXml(name):
    ''' str -> list of lxml.etree._Element

        ���������� ���������� XML ����� (����� ���� ���� � zip) � ����
        ������ ���������.
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

        �� ����������� ������ \a nodes ����������� ������� � ������ \a name,
        � ������� �������� ������ ����������� �������� �������� �������� �
        \a fields:
        'keys' - �������� ���� (��� ����, ������� ���������� ����� �����),
        'value' - �������� ������,
        'date' - �������� �� ������������ ���� (\a DATE_END).   
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

        ����� �� ����� ����������� \a name. 
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
     


      
