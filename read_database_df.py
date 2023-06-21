import pandas as pd

# Read the text file
path_wos = "./raw_data/wos_tab_3105.txt"
path_scielo = "./raw_data/scielo_3105_tab.txt"
path_scopus = "./raw_data/scopus_3105.csv"

path_wos_br = "./raw_data/wos_tab_3105.txt"
path_scielo_br = "./raw_data/scielo_tab_3105_brpt.txt"
path_scopus_br = "./raw_data/scopus_3105.csv"

df_wos = pd.read_table(path_wos, delimiter='\t')  
df_scielo = pd.read_table(path_scielo_br, delimiter='\t')
df_scopus = pd.read_csv(path_scopus, delimiter =',')

df_scielo.to_csv(r'./new_data/tab_scielobr_3105.csv', index=False)

common_columns = list(set(df_wos.columns) & set(df_scielo.columns))

# Create new dataframes with common columns
df_wos = df_wos[common_columns]
df_scielo = df_scielo[common_columns]
concat_df = pd.concat([df_wos, df_scielo])

print(concat_df.head(10))
print(len(concat_df))

print(df_scopus.columns)