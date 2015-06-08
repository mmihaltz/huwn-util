import codecs
import re
import sys

"""
Read huwn_new: ids + definitions
Read huwn_old: if id was in new and def is changed, write with new def, otherwise write unchanged
Print changed defs + ids to stdout
"""

huwn_old='../huwn_2009_visdic/huwn.xml'
huwn_old_encoding="ISO-8859-2"
huwn_new='../huwn/huwn.xml'
huwn_new_encoding="UTF-8"
outfile='huwn_2009_newdefs.xml'
outfile_encoding="ISO-8859-2"

defs = dict() # {id: def}
for line in codecs.open(huwn_new, encoding=huwn_new_encoding):
  if line.startswith('<SYNSET>'):
    m = re.search(r'<DEF>([^<]+)</DEF>', line)
    if m is not None:
      defn = m.group(1)
      m2 = re.search(r'<SYNSET><ID>([^<]+)</ID>', line)
      if m2 is not None:
        id = m2.group(1)
        defs[id] = defn

outp = codecs.open(outfile, mode='w', encoding=outfile_encoding)

for line in codecs.open(huwn_old, encoding=huwn_old_encoding):
  if line.startswith('<SYNSET>'):
    m = re.search(r'<DEF>([^<]+)</DEF>', line)
    if m is not None:
      olddef = m.group(1)
      m2 = re.search(r'<SYNSET><ID>([^<]+)</ID>', line)
      if m2 is not None:
        id = m2.group(1)
        if id in defs:
          newdef = defs[id]
          if not newdef.endswith('.'):
            newdef += '.'
          if newdef != olddef:
            line = re.sub(r'<DEF>[^<]+</DEF>', '<DEF>'+newdef+'</DEF>', line)
            print('{}\t{}'.format(id, newdef))
  outp.write(line)
