import spacy

#### ENTIDADES NOMEADAS
nlp = spacy.load("pt_core_news_sm")
#
def process_document(doc):
    return nlp(doc)
#
processed_docs = []
for doc_list in big_diarios:
    processed_doc_list = []
    for doc in doc_list:
        processed_doc = process_document(doc)
        processed_doc_list.append(processed_doc)
    processed_docs.append(processed_doc_list)
#
#
print(processed_docs[0].ents)
#
### LEMATIZAÇÃO...###
##############################