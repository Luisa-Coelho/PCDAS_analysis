import functions

filepaths = ['./raw_data/notab_wos_1105.txt','./raw_data/scopus_new_ris270423.ris', './raw_data/scielo_notab_0405.txt']
#filepaths = ['./notab_wos_1105.txt','./scielo_notab_0405.txt']

#in_file=open("./scielo_notab_0405.txt",'r',encoding="utf8")

#for filepath in filepaths:
#    # Opening all the files
#    with open(filepath, 'r', encoding='utf-8') as f:
#        functions.join_bibdata_wos_format(filepath)      
    
functions.join_bibdata_wos_format(filepaths)       
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
    
import matplotlib.pyplot as plt
# Data years = range(2000, 2023) db_scopus = [X1, X2, ..., X22] 
# # Replace X1...X22 with actual values db_wos = [Y1, Y2, ..., Y22] 
# # Replace Y1...Y22 with actual values 
# # Create the graph plt.plot(years, db_scopus, label='DB Scopus') 
# plt.plot(years, db_wos, label='DB WOS') 
# # Customize the graph plt.xlabel('Years') 
# plt.ylabel('Data') plt.title('DB Scopus vs DB WOS') 
# plt.legend() # Display the graph plt.show() 
