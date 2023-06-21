import functions 
import nltk
import spacy

file=open("./new_data/joined_bib_FINAL.txt",'r',encoding="utf8")
list_ab, list_keywords, list_language, list_address, list_type = functions.preprocess_tolist(file)

#print(list_ab[2])
nlp = spacy.load('en_core_web_sm')

list_test = []
for abstract in list_ab:
    tokenized = nlp(abstract)
    #abstract = nltk.tokenize.sent_tokenize(abstract)
    for token in tokenized:
        print(token)
    #list_test.append(output)
    
print(list_test[1])
#print(token)