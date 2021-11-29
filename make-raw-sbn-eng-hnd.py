import sys
import os
import re

with open(sys.argv[1], 'r') as f:
    nmt_prob_sent = f.readlines()

#read all the raw_sbn files and put it
# in a single file with Hindi.

#read sbn files
dirs = sorted(os.listdir(sys.argv[2]))
sbn = []
for d in dirs:
    with open(sys.argv[2]+'/'+d, 'r') as f:
        sbn.append(f.readlines())

f = open('nmt-prob-sbn.txt', 'w')

for s in nmt_prob_sent:
    for sent in sbn:
        eng = sent[0].strip()
        eng1 = re.sub(r'\.$', '', eng)
        if eng1 in s:
            print(s.strip())
            for l in sent:
                print(l.strip())
            print('######')
            break

