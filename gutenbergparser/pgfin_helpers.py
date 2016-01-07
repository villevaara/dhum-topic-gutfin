
import gensim
from gensim.parsing.preprocessing import STOPWORDS


def tokenize(text):
    return [token for token in gensim.utils.simple_preprocess(text) if token not in STOPWORDS]


def read_ta_index(indexfile, index_number):
    with open(indexfile, "r") as text_file:
        # ta_rows = text_file.readlines()
        for row in text_file:
            row = row[:-1]
            row = row.split("_")
            if str(row[0]) == str(index_number):
                bookinfo = (str(row[2]) + ": " + str(row[1]))
                return bookinfo
    return "Not found!"
