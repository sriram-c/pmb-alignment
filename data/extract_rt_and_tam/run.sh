#Extracting K layer root and tam info , O/p: anu_root.dat
echo "Extracting K layer root and Tam info..."
python3 $HOME_alignment/extract_rt_and_tam/extract_anu_root_nd_tam.py id_Apertium_input.dat > anu_root.dat

echo "Extract verb info.."
python3 $HOME_alignment/extract_rt_and_tam/extract_verb_info.py hindi_dep_parser_original_without_punc.tsv  > verb_data
#python3 $HOME_alignment/extract_rt_and_tam/extract_verb_info.py hindi_dep_parser_original.dat  > verb_data
echo "Extract root and tam info for a verb.."
#python3 $HOME_alignment/extract_rt_and_tam/verb_8_11_19.py verb_data > verb_root_tam_info
#Disable above programme written by Yukwi and started using below programme. Written by Roja(11-03-20)
python3 $HOME_alignment/extract_rt_and_tam/extract_man_root_and_tam.py verb_data  $HOME_alignment/extract_rt_and_tam/dict_tam_req.txt > verb_root_tam_info 

echo "Extract kriyA_mUla Root and ids info..."
#Get ids for verb root , extracting verb root for kriyA mUla O/p: verb_root_tam_info.dat
python3 $HOME_alignment/extract_rt_and_tam/get_manual_root_nd_tam.py  $HOME_alignment/dics/kriyA_mUla_default_dic.txt  $HOME_alignment/dics/kriyA_mUla.txt_wx $HOME_alignment/dics/verb_default_dic.txt > verb_root_tam_info.dat

echo "Alignining Verb using tam..."
python3 $HOME_alignment/extract_rt_and_tam/get_K_layer_align_using_tam_info.py

echo "Aligning Verb..."
#Verb Alignment, O/p: H_alignment_parserid-new.csv
python3 $HOME_alignment/extract_rt_and_tam/verb_alignment.py  verb_root_tam_info.dat anu_root.dat > tam_info.dat

sed -i 's/\([^(]\)(/\1OPEN-PAREN/g'  verb_root_tam_info.dat
sed -i 's/)\([^$]\)/CLOSED-PAREN\1/g'  verb_root_tam_info.dat


