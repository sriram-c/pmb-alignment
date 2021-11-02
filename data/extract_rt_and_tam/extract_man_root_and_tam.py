import sys, os, re 

tam_dic = {}
my_list = []

for line in open(sys.argv[2]):
    lst = line.strip().split()
    if lst[1] not in tam_dic.keys():
        tam_dic[lst[1]] = lst[0]
    else:
        tam_dic[lst[1]] = tam_dic[lst[1]] + '/' + lst[0]


#for key in sorted(tam_dic):
#    print(key + '\t' + tam_dic[key])


for line in open(sys.argv[1]):
#    print(line.strip())
    lst = line.strip().split()
    path = os.getenv('HOME_anu_test')
    morph_command = 'echo ' + lst[0] + ' | lt-proc -ca ' + path + '/bin/hi.morf.bin'
    #print(morph_command)
    out=os.popen(morph_command).readlines()
    analysis = out[0].split('/')
    root = '' 
    rt = []
    cat = ''
    gen = ''
    num = ''
    per = ''
    tam = ''
    TAM = ''
    out = []
    for i in range(0, len(analysis)):
        if i != 0:
            root = analysis[i].split('<')[0] 
            cat = re.findall(r'cat:([a-z]+)\>', analysis[i])
            if cat != [] and cat[0] == 'v' and root not in rt : 
                rt.append(root)
            elif cat != [] and cat[0] != 'v':
                root = ''
            gen = re.findall(r'gen:([a-z]+)\>', analysis[i]) 
            num = re.findall(r'num:([a-z]+)\>', analysis[i]) 
            per = re.findall(r'per:([a-z_]+)\>', analysis[i]) 
            tam = re.findall(r'tam:([a-zA-Z0-9]+)\>', analysis[i]) 
            if tam != []:
                if len(lst) > 1:
                    TAM = tam[0] + '_' + '_'.join(lst[1:])
                else:
                    TAM = tam[0] 
            if TAM in tam_dic.keys():
                val = tam_dic[TAM].split('/')
                for each in val:
                    v = each.split(',')
                    v[1] = gen[0]
                    if root != '':
                        m_analysis = 'root:' + root + '+' 'tam:' + v[0] + '(' + ','.join(v[1:]) + ')'
                    if m_analysis not in out:
                        out.append(m_analysis)
#    print(rt)            
#    print(out, tam)
    #if tam != [] and out != []:
    if out != []:
        print(line.strip())
        for each in out:
            m_a = each.split('+')
            print('\n'.join(m_a))
        print('---')
