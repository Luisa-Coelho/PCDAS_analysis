library('bibliometrix')
#update.packages("bibliometrix")

#file <- bib('export_scielo.bib')
## Aria, M. & Cuccurullo, C. (2017) bibliometrix: An R-tool for comprehensive science mapping analysis, 
##                                  Journal of Informetrics, 11(4), pp 959-975, Elsevier.
#https://www.bibliometrix.org/vignettes/Introduction_to_bibliometrix.html


dt_scopus <- convert2df(file = "scopus_new_270423.bib", dbsource = "isi", format = "bibtex") 
dt_wos <- convert2df(file = "wos_new_270423.bib", dbsource = "isi", format = "bibtex") 
#analytics tools from clarivate - Scielo...

results_wos <- biblioAnalysis(dt_wos, sep = ";")
results_scopus <- biblioAnalysis(dt_scopus, sep = ";")

options(width=100)
summary_wos <- summary(object = results_wos, k = 10, pause = FALSE)
summary_scopus <- summary(object = results_scopus, k = 10, pause = FALSE)

plot(x = results_wos, k = 10, pause = FALSE)
plot(x = results_scopus, k = 10, pause = FALSE)

NetMatrix <- biblioNetwork(dt_scopus, analysis = "co-occurrences", network = "keywords", sep = ";")
