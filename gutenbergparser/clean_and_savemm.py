# coding=utf-8

import logging
import tarfile
import itertools

from nltk import stem

import gensim
from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess

from pgfin_timing import Timer

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore


# datafile = ('./data/pg-fin-utf8-testdata.tar.gz')
datafile = ('./data/pg-fin-utf8.tar.gz')


def get_title(linelist):
    for line in linelist:
        line.strip()
        if line.startswith("Title: "):
            title = line[7:]
            return title
    return "Unknown"


def get_author(linelist):
    for line in linelist:
        line.strip()
        if line.startswith("Author: "):
            author = line[8:]
            return author
    return "Unknown"


def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]


def stem_token(token):
    fstemmer = stem.snowball.FinnishStemmer()
    stemtoken = token
    # was getting some funny encoding errors, this worked, finally
    try:
        stemtoken = unicode(stemtoken)
    except UnicodeDecodeError:
        stemtoken = stemtoken.decode('utf8')
    return fstemmer.stem(stemtoken)


def stem_tokens(tokens):
    stemmed_tokens = []
    for token in tokens:
        stemmed_token = stem_token(token)
        stemmed_tokens.append(stemmed_token)
    return stemmed_tokens


def process_raw_booktext(booktext):
    booktext = booktext.strip()
    linelist = booktext.splitlines()
    # for x in range(0, 10):  # debug
    #     print linelist[x]
    #     print "   ROW"
    title = get_title(linelist)
    author = get_author(linelist)
    content = "".join(linelist[32:-400])
    tokens = tokenize(content)
    stemmed_tokens = stem_tokens(tokens)
    # This might strip too much at the end. Who knows / who cares ?!
    # better option would be to detect the number of the ending metaline.
    return title, author, stemmed_tokens


# processed_testbook = process_raw_booktext(testbook)
# print processed_testbook[0]  # title
# print processed_testbook


# returns a list, add checks
def iter_data(datafile):
    with tarfile.open(datafile, 'r:gz') as tf:
        booktext_list = []
        for file_info in enumerate(tf):
            booktext = tf.extractfile(file_info).read()
            bookdata = process_raw_booktext(booktext)
            booktext_list.append(bookdata)
        return booktext_list


# yields a stream
def iter_data_to_stream(datafile, log_every=None):
    extracted = 0
    with tarfile.open(datafile, 'r:gz') as tf:
        for file_number, file_info in enumerate(tf):
            if file_info.isfile():
                if log_every and extracted % log_every == 0:
                    logging.info("extracting booktext file #%i: %s" % (extracted, file_info.name))
                booktext = tf.extractfile(file_info).read()
                yield process_raw_booktext(booktext)
                extracted += 1


class CorpusPGFin(object):
    def __init__(self, fname, ta_indexfile='./data/ta_index.txt'):
        self.fname = fname
        self.ta_indexfile = ta_indexfile

    def __iter__(self):
        for book in iter_data_to_stream(self.fname):
            yield book

    # returns stream of tokens in books
    def get_token_stream(self):
        for book in iter_data_to_stream(self.fname):
                yield book[2]

    # write title/author index to .txt file. SQL would make a lot more sense. Very slow method.
    def build_ta_index(self):
        clock = Timer()
        ta_index = ""
        index = 0
        for book in iter_data_to_stream(self.fname):
            if index % 50 == 0:
                print "Processing bookindex #" + str(index)
                clock.print_lap()
            title = book[0]
            author = book[1]
            ta_row = str(index) + "_" + str(title) + "_" + str(author) + "\n"
            index += 1
            ta_index += ta_row
        print "\n    Done!\n"
        clock.print_lap()
        clock = None
        print "\n    Writing to file " + str(self.ta_indexfile) + " ...\n"
        with open(self.ta_indexfile, "w") as text_file:
            text_file.write(ta_index)


class CorpusPGFinBOW(object):
    def __init__(self, dump_file, dictionary, clip_docs=None):
        self.dump_file = dump_file
        self.dictionary = dictionary
        self.clip_docs = clip_docs

    def __iter__(self):
        self.titles = []
        self.authors = []
        for title, author, tokens in itertools.islice(
                                                      iter_data_to_stream(self.dump_file),
                                                      self.clip_docs):
            self.titles.append(title)
            self.authors.append(author)
            yield self.dictionary.doc2bow(tokens)

    def __len__(self):
        return self.clip_docs


tokenized_corpus = CorpusPGFin(datafile)

# save title/author index
print "\n    Saving T/A index to disk.\n"
tokenized_corpus.build_ta_index()
# testing
# print (tokenized_corpus.read_ta_index(12))


print "\n    Starting document stream."
doc_stream = (tokenized_corpus.get_token_stream())
print "        doc_stream type: " + str(type(doc_stream))
print "\n"

clock = Timer()

print "\n   Creating dictionary."
id2word_pgfin = gensim.corpora.Dictionary(doc_stream)
print (id2word_pgfin)

clock.print_lap()

# filter tokens: discard those in less than 2 documents and those in more than 40%
# leaves about 10% with test set of 20
id2word_pgfin.filter_extremes(no_below=10, no_above=0.7)
print (id2word_pgfin)

print "\n    Saving dictionary to disk.\n"
# id2word_pgfin.save('./data/pgfintestdata20.dictionary')
id2word_pgfin.save('./data/pgfin.dictionary')

clock.print_lap()

# create a stream of bag-of-words vectors
pgfin_bow_corpus = CorpusPGFinBOW(datafile, id2word_pgfin)

print "\n    Saving bag-of-words corpus to disk.\n"
# gensim.corpora.MmCorpus.serialize('./data/pgfin_testdata20_bow.mm', pgfin_bow_corpus)
gensim.corpora.MmCorpus.serialize('./data/pgfin_bow.mm', pgfin_bow_corpus)

clock.print_lap()
clock = None
