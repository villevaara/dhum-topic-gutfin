# coding=utf-8

import logging

import gensim
from gensim.similarities import Similarity, MatrixSimilarity

# from pgfin_timing import Timer

from pgfin_helpers import tokenize


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


# load the corpora

print "\n    Loading corpora.\n"
# tfidf_corpus = gensim.corpora.MmCorpus('./data/pgfintestdata20_tfidf.mm')
# lsi_corpus = gensim.corpora.MmCorpus('./data/pgfintestdata20_lsa.mm')
# tfidf_corpus = gensim.corpora.MmCorpus('./data/pgfin_tfidf.mm')
lsi_corpus = gensim.corpora.MmCorpus('./data/pgfin_lsa.mm')
# print(tfidf_corpus)
# print(lsi_corpus)

print "\n    Start similarity index.\n"
index = Similarity('./data/pgfin_index', lsi_corpus, num_features=lsi_corpus.num_terms)
index.save('./data/pgfin_index.index')  # save to disk
# print index
index_dense = MatrixSimilarity(lsi_corpus, num_features=lsi_corpus.num_terms)
index_dense.save('./data/pgfin_matrixindex.index')  # save to disk
# print index_dense
