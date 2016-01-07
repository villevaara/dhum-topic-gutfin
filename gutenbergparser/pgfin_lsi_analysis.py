# coding=utf-8

import logging

import gensim

# from pgfin_timing import Timer


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

print "\n    Loading dictionary and corpus.\n"
# id2word_pgfin = gensim.corpora.dictionary.Dictionary.load('./data/pgfintestdata20.dictionary')
# pgfin_corpus = gensim.corpora.MmCorpus('./data/pgfin_testdata20_bow.mm')
id2word_pgfin = gensim.corpora.dictionary.Dictionary.load('./data/pgfin.dictionary')
pgfin_corpus = gensim.corpora.MmCorpus('./data/pgfin_bow.mm')


print "\n    Creating tf-idf model.\n"
tfidf_model = gensim.models.TfidfModel(pgfin_corpus, id2word=id2word_pgfin)
# print tfidf_model
print "\n    Creating lsi model.\n"
lsi_model = gensim.models.LsiModel(tfidf_model[pgfin_corpus], id2word=id2word_pgfin, num_topics=200)
# print lsi_model

# store models to disk
print "\n    Saving models.\n"
# lsi_model.save('./data/lsi_pgfintestdata20.model')
# tfidf_model.save('./data/tfidf_pgfintestdata20.model')
lsi_model.save('./data/lsi_pgfin.model')
tfidf_model.save('./data/tfidf_pgfin.model')

# store transformed corpus to disk
print "\n    Storing transformed corpus to disk.\n"
# gensim.corpora.MmCorpus.serialize('./data/pgfintestdata20_tfidf.mm',
#                                   tfidf_model[pgfin_corpus])
# gensim.corpora.MmCorpus.serialize('./data/pgfintestdata20_lsa.mm',
#                                   lsi_model[tfidf_model[pgfin_corpus]])
gensim.corpora.MmCorpus.serialize('./data/pgfin_tfidf.mm',
                                  tfidf_model[pgfin_corpus])
gensim.corpora.MmCorpus.serialize('./data/pgfin_lsa.mm',
                                  lsi_model[tfidf_model[pgfin_corpus]])
