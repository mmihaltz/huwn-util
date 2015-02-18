#!/usr/bin/env python3
# coding: utf8

"""
Fixes to huwn.xml:
- fix sense numbers: no duplicates, consecutive numbering (starting from 1) for literals in a PoS, trying to preserve original order
- internal relations lists uniq'ed in synsets
- XML now contains inverted relations as well
- no LF characters

Author: Marton Mihaltz <mmihaltz@gmail.com>

Requires pywnxml (https://github.com/ppke-nlpg/pywnxml).
"""

import os
import sys
sys.path.append('/home/mm/NYTI/PyWNXML')
import WNQuery


if len(sys.argv) != 3:
  sys.exit('Parameters: input output\n')

# Open output file
out = open(sys.argv[2], 'w')

# Load HuWN
sys.stderr.write('Reading XML...\n')
wn = WNQuery.WNQuery(sys.argv[1], open(os.devnull, "w"))
sys.stderr.write('Done\n')

# Fix sense numbers
sys.stderr.write('Fixing sense numbers...\n')
for index, data in [(wn.m_nidx, wn.m_ndat), (wn.m_vidx, wn.m_vdat), (wn.m_aidx, wn.m_adat), (wn.m_bidx, wn.m_bdat)]:
  for literal in sorted(index.keys()):
    senses = [] # [(Synset, sense), ...]
    ssets = index[literal]
    for ssid in sorted(ssets):
      ss = data[ssid]
      for syn in ss.synonyms:
        if syn.literal == literal:
          senses.append((ss, syn.sense))
    for newsense, (ss, sense) in enumerate(sorted(senses, key=lambda x: int(x[1]))):
      print('{}\t{}\t{}\t{}'.format(ss.wnid, literal, sense, newsense+1))
      for syn in ss.synonyms:
        if syn.literal == literal:
          syn.sense = str(newsense+1)

# Write XML back to file
sys.stderr.write('Writing XML...\n')
out.write("""<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE WNXML SYSTEM "wnxml.dtd">
<!--
Hungarian WordNet release 2015-02-18
Contact: mmihaltz@gmail.com
See README.txt for more information.
-->
<WNXML>\n""")
for data in [wn.m_ndat, wn.m_vdat, wn.m_adat, wn.m_bdat]:
  for ssid in sorted(data.keys()):
    sset = data[ssid]
    sset.writeXML(out)
    out.write('\n')
out.write('</WNXML>\n')
out.close()
sys.stderr.write('Done.\n')

