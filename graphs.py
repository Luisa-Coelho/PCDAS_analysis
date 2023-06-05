import matplotlib.pyplot as plt 
import numpy as np

def count_years(filename):
    year_counts = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if 'PY' in line:
                year = line.strip().split('PY')[1].strip()
                if year in year_counts:
                    year_counts[year] += 1
                else:
                    year_counts[year] = 1
    return year_counts

def count_years_base(filename):
    # Open the text file
    #year_counts = {}
    year_wos = {}
    year_scielo = {}
    year_scopus = {}
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Iterate over the lines and extract the desired lines
    extracted_lines = []
    for line in lines:

        if 'PY' in line:
            year = line.strip().split('PY')[1].strip()
                
        if "WEB OF SCIENCE" in line:
            if year in year_wos:
                year_wos[year] += 1
            else:
                year_wos[year] = 1
            
        if "SCOPUS" in line:
            if year in year_scopus:
                year_scopus[year] += 1
            else:
                year_scopus[year] = 1
                
        if "SCIELO" in line:
            if year in year_scielo:
                year_scielo[year] += 1
            else:
                year_scielo[year] = 1
                
    return year_scielo, year_scopus, year_wos
            
count = count_years("./new_data/joined_bib.txt")
y_scielo, y_scopus, y_wos = count_years_base("./new_data/joined_bib.txt")
print(y_scielo, y_scopus, y_wos)

###############################################
################ GRÁFICO TOTAL ################
############################################### 
count = dict(sorted(count.items()))
years = list(count.keys())
values = list(count.values())

fig = plt.figure( )

# Creating the bar graph
plt.bar(years, values)

plt.bar(years, values,
        width = 0.8, color = ['purple'])

# Rotating x-axis labels for better readability
plt.xticks(rotation=45)

# Adding labels and title
plt.xlabel('Anos')
plt.ylabel('Quantidade de Publicações')

fig.savefig('./new_data/publicacoes_total.jpg', bbox_inches='tight', dpi=150)
# Displaying the graph
plt.show()

####################################################################
############### GRÁFICO BASES ######################################
###################################################################

years = sorted(set(y_scopus.keys()) | set(y_scielo.keys()) | set(y_wos.keys()))
values1 = [y_scopus.get(year, 0) for year in years]
values2 = [y_scielo.get(year, 0) for year in years]
values3 = [y_wos.get(year, 0) for year in years]

fig = plt.figure( )
# Plot the bar graph
plt.figure(figsize=(10, 6))
plt.bar(years, values1, label='Scopus')
plt.bar(years, values2, label='Scielo')
plt.bar(years, values3, label='Web of Science - Coleção principal')

plt.xlabel('Anos')
plt.ylabel('Quantidade de publicações')

plt.xticks(rotation=45)

plt.legend()
plt.show()

fig.savefig('./new_data/publicacoes_bases.jpg', bbox_inches='tight', dpi=150)