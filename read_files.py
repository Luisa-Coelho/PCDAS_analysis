import functions

#filepaths = ['./raw_data/wos_3105.txt','./raw_data/scielo_3105.txt', './raw_data/scopus_3105.ris']
filepaths = ['./raw_data/macauba_wos.txt', './raw_data/macauba_scielo.txt']

functions.join_bibdata_wos_format(3, filepaths)
in_file=open("./new_data/joined_3.txt",'r',encoding="utf8")

### ATENTE-SE ao nome do arquivo, ELE TEM QUE ter OU wos OU scielo OU scopus...
#(n_authors, n_authors, years, types, tc, nr) = functions.join_bibdata_wos_format(1, filepaths)
#print(n_authors)
#print(years)
#print(types)
#print(tc)
#
dois, tis = functions.check_doi(in_file)
print("DOIS")
for doi in dois:
    print(f'{doi}\n')
print("TITLES")
for ti in tis:
    print(f'{ti}\n')