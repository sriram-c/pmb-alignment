#Program to align example sentences
import sys
import re

def get_root(morph):
    root_wds = {}
    for wd in morph.split():
        roots = wd.split('/')
        rt_list = []
        for rt in roots:
            if '<' in rt:
                root_wd = re.match(r'^([^<])*', rt)[0]
                rt_list.append(root_wd)
            elif '^' in rt:
                org_wd = re.match(r'^\^(.*)$', rt)[1]
        root_wds[org_wd] = list(set(rt_list))
    return root_wds


def lwg_process(e_h_lwg):

    #For lwg give root and keep other words not to search
    #are_cutting    root:cut tam:are_ing ('are' not search)(are: rahe_hEM)

    lwg_dic = {}

    lwg_wd = e_h_lwg.split('\t')[0].split('_')
    lwg_hwd = e_h_lwg.split('\t')[5].split('_')
    lwg_root = e_h_lwg.split('\t')[1]
    lwg_aux = e_h_lwg.split('\t')[2]
    lwg_hindi = e_h_lwg.split('\t')[3]

    if '_' in lwg_aux:
        lwg_aux = lwg_aux.split('_')[:-1]
    if '0' in lwg_hindi:
        lwg_hindi = lwg_hindi.split('_')[1:]

    lwg_dic['_'.join(lwg_aux)] = lwg_hindi

    return lwg_wd, lwg_hwd


def align(E_H_sen, E_morph, H_morph, e_h_lwg, E_H_dic_processed, E_H_controlled_dic_processed):

    # function to align the English and Hindi sen
    # input : E_sen, H_sen, E_H_dic, E_H_dic controlled (user made)
    # output: aligned words

    E_wds = E_H_sen.split('\t')[0].split()
    H_wds = E_H_sen.split('\t')[1].split()
    E_root_wds = get_root(E_morph)
    H_root_wds = get_root(H_morph)

    #add all root words in hindi list
    for key in H_root_wds:
        H_wds.extend(H_root_wds[key])


    E_H_aligned = {}

    #match original word
    for ewd in E_wds:
        h_dic_wd = []
        if ewd.lower() in E_H_dic_processed:
            h_dic_wd.extend(E_H_dic_processed[ewd.lower()])

        for rt_wd in E_root_wds[ewd]:
            if rt_wd.lower() in E_H_dic_processed:
                h_dic_wd.extend(E_H_dic_processed[rt_wd.lower()])

        for hwd in h_dic_wd:
            if hwd in H_wds:
                E_H_aligned[ewd] = hwd
                break


    #for lwg processing
    if len(e_h_lwg) > 0:
        lwg_wd, lwg_hwd = lwg_process(e_h_lwg)
        if set(lwg_hwd).issubset(set(H_wds)):

            E_H_aligned['_'.join(lwg_wd)] = '_'.join(lwg_hwd)

            for wd in lwg_wd:
                if wd in E_H_aligned: del E_H_aligned[wd]

    #for left over words to check meaning from controlled dic:
    for wd in E_wds:
        if wd not in E_H_aligned:
            if wd in E_H_controlled_dic_processed:
                hwd = E_H_controlled_dic_processed[wd]
                if set(wd.split('_')).issubset(set(H_wds)):
                    E_H_aligned[wd] = hwd.split('_')

    return E_H_aligned


def dic_process(E_H_dic):
    # read English-Hindi dictionary
    # store it in dictionary without the category info
    E_H_dic_processed = {}
    for line in E_H_dic:
        a =   (re.match('^#', line))
        if not(a):
            eng_wd_catg = line.split('\t')[0]
            eng_wd = eng_wd_catg.split('_')[0]
            hnd_wd = line.split('\t')[1].strip()
            hnd_wd_list = []
            if '/' in hnd_wd:
                hnd_wd_list = hnd_wd.split('/')
            else:
                hnd_wd_list.append(hnd_wd)

            if eng_wd in E_H_dic_processed:
                E_H_dic_processed[eng_wd].extend(hnd_wd_list)
            else:
                E_H_dic_processed[eng_wd] = hnd_wd_list

    return  E_H_dic_processed


#Read English Hindi dictionary
with open(sys.argv[1], 'r')as f:
    E_H_dic = f.readlines()
E_H_dic_processed = dic_process(E_H_dic)

#read English Hindi raw sentence
with open(sys.argv[2], 'r') as f:
    E_H_sen = f.readlines()

#read English morph from lt-proc
with open(sys.argv[3], 'r') as f:
    E_morph = f.readlines()

#read Hindi morph from lt-proc
with open(sys.argv[4], 'r') as f:
    H_morph = f.readlines()

#read English Hindi lwg info
with open(sys.argv[5], 'r') as f:
    E_H_lwg = f.readlines()

#read English Hindi lwg info
with open(sys.argv[6], 'r') as f:
    E_H_controlled_dic = f.readlines()
    E_H_controlled_dic_processed = {}
    for line in E_H_controlled_dic:
        eng_wd = line.split('\t')[0]
        hnd_wd = line.split('\t')[1].strip()
        E_H_controlled_dic_processed[eng_wd] = hnd_wd

for sen, e_morph, h_morph, e_h_lwg in zip(E_H_sen, E_morph, H_morph, E_H_lwg):
    E_H_aligned = align(sen.strip(), e_morph, h_morph, e_h_lwg.strip(), E_H_dic_processed, E_H_controlled_dic_processed)
    print(sen.strip())
    print(E_H_aligned)
    print('---------')

