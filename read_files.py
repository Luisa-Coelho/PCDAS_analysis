import functions

filepaths = ['./raw_data/wos_3105.txt','./raw_data/scielo_3105.txt', './raw_data/scopus_3105.ris']
filepaths_br = ['./raw_data/wosbr_3105.txt','./raw_data/scielobr_3105', './raw_data/scopusbr_3105.ris']


functions.join_bibdata_wos_format(1, filepaths)
in_file=open("./new_data/joined_bib.txt",'r',encoding="utf8")
dois, tis = functions.check_doi(in_file)
print("DOIS")
for doi in dois:
    print(f'{doi}\n')
print("TITLES")
for ti in tis:
    print(f'{ti}\n')