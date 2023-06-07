from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from deep_translator import GoogleTranslator
import matplotlib.pyplot as plt
from sklearn.feature_extraction import text
import spacy
from wordcloud import WordCloud
import pandas as pd
import plots_functions
import rispy
import datetime

df = pd.DataFrame(columns=['id', 'title', 'authors', 'abstract', 'keywords', 'year', 'source'])

#from RISparser.config import TAG_KEY_MAPPING
filepaths = ['./scopus_new_ris270423.ris', './scielo_ris_new270423.ris', './wos_new_ris270423.ris']

# Extract the titles of the references
#count = 0
for filepath in filepaths:
      # Open the RIS file
    with open(filepath, 'r', encoding='utf-8') as f:
        # Parse the RIS file
        records = rispy.load(f)
        
        for record in records:
            id = record.get('id', '')
            title = record.get('title', '')
            authors = record.get('authors', [])
            abstract = record.get('abstract', '')
            keywords = record.get('keywords', [])
            year = record.get('year', '')
            journal_name = record.get('journal_name', '')
            df = df.append({
                'id': id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'keywords': keywords,
                'year': year,
                'source': journal_name
                }, ignore_index=True)

# Print the resulting dataframe
#print(len(df))

nlp = spacy.load('en_core_web_sm')
list2_ab = []
list2_keywords = []

for keywords in df['keywords'].tolist():
    key = str(keywords).split(";")
    list2_keywords.append(key)

list2_keywords = sum(list2_keywords, [])
#print(list2_keywords)

for abstract in df['abstract'].tolist():
    doc = GoogleTranslator(source='auto', target='en').translate(abstract)
    list2_ab.append(doc)
    
#list2_ab

my_additional_stop_words = ['2000']

list2_ab = [w for w in list2_ab if w not in my_additional_stop_words]

#list2_ab = " ".join(list2)

#list_nlpab = [nlp(keywords) for keywords in list2_ab]
#list_nlpkey = [nlp(keywords) for keywords in list2_keywords]

#tokens_ab = [token.lemma_ if token.pos_ == "VERB" else str(token) for token in list_nlpab]

tfidf = TfidfVectorizer(min_df=1, max_df= 20, stop_words='english')
#dtm = tfidf.fit_transform(list2_keywords)
dtm = tfidf.fit_transform(list2_ab)

nmf_model = NMF(n_components=8,random_state=None, beta_loss='kullback-leibler', solver='mu')           
nmf_model.fit(dtm)
tfidf_feature_names = tfidf.get_feature_names_out()

date = datetime.datetime.now()
date = print(date)

plots_functions.plot_NMF(
    nmf_model, tfidf_feature_names, 20, "", f'all_db_abstract_{date}', "kullback"
)
