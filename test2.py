import rispy
import pandas as pd

#import litstudy
#from pprint import pprint
#from RISparser import readris

#docs_scopus = litstudy.load_ris_file('./scopus_new_ris270423.ris')
#docs_wos = litstudy.load_ris_file('./wos_new_ris270423.ris')
#docs_scielo = litstudy.load_ris_file('./scielo_ris_new270423.ris')
Path = (".")

#df_ris = {
#    'articles': {
#        'id': '',
#        'authors': [],
#        'title': '',
#        'keywords': [],
#        'abstract': '',
#        'year': '',
#        'source': ''
#    }
#}

df = pd.DataFrame(columns=['id', 'title', 'authors', 'abstract', 'keywords', 'year', 'source'])

#from RISparser.config import TAG_KEY_MAPPING
filepath = './scopus_new_ris270423.ris'
# Open the RIS file
with open(filepath, 'r', encoding='utf-8') as f:
    # Parse the RIS file
    records = rispy.load(f)

# Extract the titles of the references
#count = 0
for record in records:
    id = record.get('id', '')
    title = record.get('title', '')
    authors = record.get('authors', [])
    abstract = record.get('abstract', '')
    keywords = record.get('keywords', [])
    year = record.get('year', '')
    source = record.get('source', '')
    df = df.append({
        'id': id,
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'keywords': keywords,
        'year': year,
        'source': source
    }, ignore_index=True)

# Print the resulting dataframe
print(df.head())


#with open(filepath, 'r', encoding='utf-8') as bibliography_file:
#    entries = readris(bibliography_file)
#    for entry in  entries:
#        print(entry['ID'])
#        print(entry['AU'])
#        #if entry.get('ID', '') not in df_ris['id'].tolist():
        #    df_ris = df_ris.append({
        #        'ID': entry['id'],
        #        'authors': entry.get('AU', '')}, ignore_index=True)

#mapping = TAG_KEY_MAPPING
#mapping["SP"] = "pages_this_is_my_fun"
#with open(filepath, 'r', encoding='utf-8') as bibliography_file:
#    entries = readris(bibliography_file, mapping=mapping)
#    #pprint(sorted(entries[0].keys()))    
#    for entry in entries:
#        print(entry)  
#        print("\n \n \n \n")         
#            
#print(df_ris)7

      