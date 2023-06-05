import functions

filepaths = ['./raw_data/wos_3105.txt','./raw_data/scielo_3105.txt', './raw_data/scopus_3105.ris']
filepaths_br = ['./raw_data/wosbr_3105.txt','./raw_data/scielobr_3105', './raw_data/scopusbr_3105.ris']

functions.join_bibdata_wos_format(filepaths)

in_file=open("./new_data/joined_bib.txt",'r',encoding="utf8")
dois = functions.check_doi(in_file)   

#in_file=open("./scielo_notab_0405.txt",'r',encoding="utf8")

#for filepath in filepaths:
#    # Opening all the files
#    with open(filepath, 'r', encoding='utf-8') as f:
#        functions.join_bibdata_wos_format(filepath)      
 
#lines = in_file.readlines()
#new = functions.transf_txt_to_ris(lines)

#print(new)

def count_years(filename):
    year_counts = {}
    with open(filename, 'r') as file:
        for line in file:
            if 'PY' in line:
                year = line.strip().split('PY')[1].strip()
                if year in year_counts:
                    year_counts[year] += 1
                else:
                    year_counts[year] = 1
    return year_counts

#filename = 'your_file.txt'  # Replace with the actual path to your text file
##year_counts = count_years(filename)

#for3 year, count in year_counts.items():
#    print(f"{year}: {count}")
    

