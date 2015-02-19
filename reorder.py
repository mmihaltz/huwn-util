#!/usr/bin/env python3
# Parse HuWN XML and reorder children of SYNSET as prescribed by the DTD

import sys
import xml.etree.ElementTree as ET

ORDER = ['ID', 'ID3', 'POS', 'SYNONYM', 'ILR', 'DEF', 'BCS', 'USAGE', 'SNOTE', 'STAMP', 'DOMAIN', 'SUMO', 'NL', 'TNL', 'ELR', 'ELR3', 'EQ_NEAR_SYNONYM', 'EQ_HYPERNYM', 'EQ_HYPONYM', 'EKSZ', 'VFRAME']
ORDMAP = dict([(y, x) for x, y in enumerate(ORDER)])

tree = ET.parse(sys.argv[1])
root = tree.getroot()

newroot = ET.Element('WNXML')

for syn in root.getiterator('SYNSET'):
  newsyn = ET.Element('SYNSET')
  for ch in sorted(syn.getchildren(), key=lambda x: ORDMAP[x.tag]):
    newsyn.append(ch)
  #ET.SubElement(newroot, newsyn)
  print(ET.tostring(newsyn, encoding='utf8').decode('utf8'))

#newtree = ET.ElementTree(newroot)
#print(ET.tostring(newtree, encoding='utf8'))
#newtree.write('ordered.xml', encoding='utf8')
