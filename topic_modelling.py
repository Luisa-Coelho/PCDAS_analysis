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
import functions
import datetime
import string

file=open("./new_data/joined_bib_FINAL.txt",'r',encoding="utf8")
list_ab, list_keywords, list_language, list_address, list_type = functions.preprocess_tolist(file)

nlp = spacy.load('en_core_web_sm')

list2_ab = []
list3_ab = []  
for abstract in list_ab:
    if len(abstract) > 5000 or len(abstract) < 0:
        list3_ab.append(abstract)
    else:
        doc = GoogleTranslator(source='auto', target='en').translate(abstract)
        list2_ab.append(doc)

for big_ab in list3_ab:
    print(big_ab)
    print(len(big_ab))
    ## do not contain info on abstracts
    
#my_additional_stop_words = ['2000']
#list2_ab = [w for w in list2_ab if w not in my_additional_stop_words]

def remove_punctuation_and_numbers(text):
    remove = str.maketrans("", "", string.punctuation + string.digits)
    text_without_punctuation_and_numbers = text.translate(remove)
    
    return text_without_punctuation_and_numbers

listnew_ab = []
for ab in list2_ab:
    new_ab = remove_punctuation_and_numbers(ab)
    listnew_ab.append(new_ab)

#nlpab = [nlp(abstract) for abstract in listnew_ab]
#tokens_ab = [token.lemma_ if token.pos_ == "VERB" else str(token) for token in nlpab[0]]
#tokens_ab = [token.lemma_ for token in nlpab[0]]

tfidf = TfidfVectorizer(min_df=2, max_df= 50, stop_words='english')
dtm = tfidf.fit_transform(listnew_ab)


nmf_model = NMF(n_components=8,random_state=42, beta_loss='kullback-leibler', solver='mu')           
nmf_model.fit(dtm)
tfidf_feature_names = tfidf.get_feature_names_out()

date = datetime.datetime.now()
datestr = date.strftime('%d%m%Y')

plots_functions.plot_NMF(
    nmf_model, tfidf_feature_names, 12, "", f'all_db_abstract_{datestr}', "kullbackrem"
)

plots_functions.plot_wordcloud(
    nmf_model, tfidf_feature_names, 15, "", f'all_db_abstract_{datestr}', "kullbacknrem"
)
