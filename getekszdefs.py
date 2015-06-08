import codecs
import re
import sys

"""
Read eksz.xml: get all definitions + their ids
then read huwn xml (utf8 version, from git), and print synset ids whose definitions are in EKSZ + the definition + the pertaining EKSZ ids
"""

ekszfile='../eksz/eksz.xml'
#huwnfile='../git/huwn.xml'
huwnfile='Pajzs_Juli_2015-05-28/huwn.utf8.xml'

eksz = dict() # {def: [ids], ...}
for line in open(ekszfile):
  if line.startswith('<SENSE>'):
    m = re.search(r'<DEF>([^<]+)</DEF>', line)
    if m is not None:
      defi = m.group(1)
      n = re.search(r'<ID>([^<]+)</ID>', line)
      if n is not None:
        id = n.group(1)
        if defi not in eksz:
          eksz[defi] = []
        eksz[defi].append(id)
#for defi in eksz:
#  print(defi, eksz[defi])

for line in codecs.open(huwnfile, encoding='utf8'):
  if line.startswith('<SYNSET>'):
    m = re.search(r'<DEF>([^<]+)</DEF>', line)
    if m is not None:
      defi = m.group(1)
      n = re.search(r'<SYNSET><ID>([^<]+)</ID>', line)
      if n is not None:
        id = n.group(1)
        if defi in eksz:
          print('{}\t{}\t{}'.format(id, defi, ','.join(eksz[defi])))
 