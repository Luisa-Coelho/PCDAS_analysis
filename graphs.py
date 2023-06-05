import matplotlib.pyplot as plt 

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

count = count_years("./new_data/joined_bib.txt")


# Extracting the years and values from the dictionary
years = list(count.keys())
values = list(count.values())

# Creating the bar graph
plt.bar(years, values)

# Adding labels and title
plt.xlabel('Anos')
plt.ylabel('Quantidade de Publicações')
#plt.title('Graph')

# Rotating x-axis labels for better readability
plt.xticks(rotation=45)

# Displaying the graph
plt.show()


years = range(2000, 2023)
# db_scopus = [X1, X2, ..., X22] #
# db_wos = [Y1, Y2, ..., Y22] #
# Create the graph 
# plt.plot(years, db_scopus, label='DB Scopus') 
# plt.plot(years, db_wos, label='DB WOS')
# # Customize the graph 
# plt.xlabel('Years') plt.ylabel('Data') 
# plt.title('DB Scopus vs DB WOS') 
# plt.legend() #
# Display the graph plt.show()