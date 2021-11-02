import sys, string

f = open(sys.argv[1], 'r').readlines()

verb_lst = []
verb = ''
for i in range(0, len(f)):
    lst = f[i].strip().split('\t')
    if lst[3] == 'VERB':
        verb == ''
        verb = lst[1].strip(string.punctuation)
    if lst[3] == 'AUX':
           verb = verb + ' ' + lst[1].strip(string.punctuation)
    if lst[3] == 'ADP' and verb != '':
           if verb not in verb_lst and verb != '':
            verb_lst.append(verb)
            verb = ''
    if lst[3] != 'VERB' and lst[3] != 'AUX' and lst[3] != 'ADP':
          if verb not in verb_lst and verb != '':
            verb_lst.append(verb.strip())
            verb = ''
    if i == len(f)-1 and verb != '' and verb not in verb_lst: #For cases handling sentence end . Ex: kara_sakawe_hEM
            verb_lst.append(verb)
            verb = ''


for each in verb_lst:
    print(each)

