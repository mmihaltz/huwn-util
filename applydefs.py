import codecs
import re
import sys

"""
Read list of ids + definitions from file 1
Read huwn from file2
Output huwn with definition changes applied
"""

deffile='./Pajzs_Juli_2015-03-03/edited_defs.changed.sort.txt'
huwnfile='../huwn/huwn.xml'
outfile='huwn_newdefs.xml'

defs = dict() # {id: def}
for line in open(deffile):
  line = line.strip()
  t = line.split('\t')
  if len(t) != 2:
    continue
  defs[ t[0] ] = t[1]

outp = codecs.open(outfile, mode='w', encoding='utf8')
for line in codecs.open(huwnfile, encoding='utf8'):
  if line.startswith('<SYNSET>'):
    m = re.search(r'<DEF>([^<]+)</DEF>', line)
    if m is not None:
      defi = m.group(1)
      n = re.search(r'<SYNSET><ID>([^<]+)</ID>', line)
      if n is not None:
        id = n.group(1)
        if id in defs:
          newdef = defs[id]
          if not newdef.endswith('.'):
            newdef += '.'
          line = re.sub(r'<DEF>[^<]+</DEF>', '<DEF>'+newdef+'</DEF>', line)
  outp.write(line)