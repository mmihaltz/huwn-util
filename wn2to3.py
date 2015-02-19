#! /usr/bin/env python
# coding=utf8
"""Add PWN30 synset ids to HuWN XML
Author: Ivan Mittelholcz
"""

import os.path
import argparse
import copy
import xml.etree.cElementTree as ET


def check_xml(xml_file):
    """Fájl létezésének és xml-ségének ellenőrzése.
        - input: fájlnév
        - output: xml tree
    """
    xml_file = os.path.abspath(xml_file)
    if not os.path.exists(xml_file):
        raise argparse.ArgumentTypeError('Nem létező fájl: ' + xml_file)
    try:
        return ET.parse(xml_file)
    except ET.ParseError:
        raise argparse.ArgumentTypeError('Nem xml fájl: ' + xml_file)

def args_handling():
    """Parancssori argumentumok kezelése.
    """
    pars = argparse.ArgumentParser(description=__doc__)
    pars.add_argument(
            'source',
            help='xml forrásfájl',
            type=check_xml,
            nargs=1)
    return vars(pars.parse_args())

def mapping(file_):
    """ID-szótárak készítése map fájlokból.
        - input: fájlnév
        - 1. oszlop: wn3 id
        - 2. oszlop: wn2 id
    """
    map_dir = '../PWN_3.0-2.0_Concept_Mapping/'
    with open(map_dir + file_, 'r') as map_:
        map_dict = dict()
        for line in map_.readlines():
            line = line.split()
            map_dict[line[1]] = line[0]
        return map_dict

def get_id3(id2):
    """ENG20-as id-k ENG30-as megfelelőinek kikeresése.
        - input: ENG20-as id (str)
        - output: ENG30-as id (str)
    """
    dic = id2[-1]
    id2 = id2[6:-2]
    id3 = ID_DICT.get(dic)
    if not id3:
        print 'Nem létező POS tag: ' + id2 + '-' + dic
        return
    id3 = id3.get(id2)
    if not id3:
        print 'Nem létező ID: ' + id2 + '-' + dic
        return
    id3 = 'ENG30-' + id3 + '-' + dic
    return id3

def process_id(synset, id2):
    """ENG20-as id alapján új ID3 tag beszúrása
        - input: eng20-at tartalmazó synset, id2 értéke
        - output: nincs, közvetlenül módosítja a csomópontot-et
    """
    id3 = get_id3(id2.text)
    if id3:
        index = list(synset).index(id2) + 1
        elem = ET.Element('ID3')
        elem.text = id3
        synset.insert(index, elem)

def process_elr(synset, elrs):
    """ELR (extern language resources?) alapján ELR3 tag beszúrása.
        - input: ELR csomóponttal (lehet több is!) bíró synset
        - output: nincs, közvetlenül módosítja a synset-et
    """
    # insert_place: az utolsó ELR utáni hely
    insert_place = [x for x, e in enumerate(synset) if e.tag == 'ELR'][-1] + 1
    for count, elr in enumerate(elrs):
        id2 = elr.text
        if not id2.startswith('ENG20'):
            continue
        id3 = get_id3(id2)
        if id3:
            # index: insert_place + az eddigi beszúrások száma
            index = insert_place + count
            elem = copy.deepcopy(elr)
            elem.tag = 'ELR3'
            elem.text = id3
            synset.insert(index, elem)


def main():
    """xml beolvasása és átalakítása
    """
    # xml-fa:
    tree = args_handling()['source'][0]
    root = tree.getroot()
    # fa bejárása:
    for synset in root.iter('SYNSET'):
        # <ID>-k feldolgozása:
        id2 = synset.find('ID')
        if id2.text.startswith('ENG20'):
            process_id(synset, id2)
        # <ELR>-ek feldolgozása:
        elrs = synset.findall('ELR')
        if elrs:
            process_elr(synset, elrs)
    # módosított fa kiírása:
    tree.write('updated.xml', 'utf-8', True)
    # ET.dump(root)
    return

if __name__ == '__main__':
    # id-szótár (globális):
    ID_DICT = dict()
    ID_DICT['a'] = mapping('adj.txt')
    ID_DICT['b'] = mapping('adv.txt')
    ID_DICT['n'] = mapping('noun.txt')
    ID_DICT['v'] = mapping('verb.txt')
    main()

