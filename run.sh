#For aligning English and Hindi sentences
#English hindi default dictionary
#lt-proc for getting morph of english words

utf8_wx E_H_sen.txt | sed -e 's/Z//'  > E_H_sen-wx.txt
cut -f 1 E_H_sen-wx.txt > eng
cut -f 2 E_H_sen-wx.txt > hnd
lt-proc -a en.morf.bin eng > eng_morph
lt-proc -c -a hi.morf.bin hnd > hnd_morph
python alignment.py  E_H_dictionary E_H_sen-wx.txt eng_morph hnd_morph lwg_eng_hnd controlled_dictionary.txt pmb-data e_h_tam_list-wx hnd_tam_all_form
