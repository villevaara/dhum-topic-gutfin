# coding=utf-8

import logging

import gensim
from gensim.similarities import Similarity, MatrixSimilarity

# from pgfin_timing import Timer

from pgfin_helpers import read_ta_index, tokenize


logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


# load models

print "\n    Loading models, etc..\n"
id2word_pgfin = gensim.corpora.Dictionary.load('./data/pgfin.dictionary')
tfidf_model = gensim.models.TfidfModel.load('./data/tfidf_pgfin.model')
lsi_model = gensim.models.LsiModel.load('./data/lsi_pgfin.model')
indexfile = ('./data/ta_index.txt')
queryfile = './queryfiles/queryfile.txt'  # text in corpus
# queryfile = './queryfiles/45vuotta.txt'  # Film review
# queryfile = './queryfiles/tktjohdessee2.txt'  # Ancient essay

# check similarity

print "\n    Load similarity indices.\n"
index = Similarity.load('./data/pgfin_index.index')
index_dense = MatrixSimilarity.load('./data/pgfin_matrixindex.index')

with open(queryfile, 'r') as datafile:
    query = datafile.read()

# vectorize the query text into bag-of-words and tfidf
query_bow = id2word_pgfin.doc2bow(tokenize(query))
query_tfidf = tfidf_model[query_bow]
query_lsi = lsi_model[query_tfidf]

index_dense.num_best = 5


class BookHitValue(object):

    def __init__(self, indexfile, author_title, hit_percent):
        self.author_title = read_ta_index(indexfile, author_title)
        self.hit_percent = hit_percent

    def __str__(self):
        hit_str = str(int(self.hit_percent*100))
        ret_str = self.author_title + " (" + hit_str + "%)"
        return ret_str


def get_book_indexes(indexlist):
    book_indexlist = ([x[0] for x in indexlist])
    return book_indexlist


def print_closest_hits(indexlist, indexfile):
    for entry in indexlist:
        print BookHitValue(indexfile, entry[0], entry[1])

print "\n    Getting closest hits for queryfile: " + str(queryfile) + " ...\n"
print_closest_hits((index_dense[query_lsi]), indexfile)
