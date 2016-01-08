# dhum-topic-gutfin
Digital Humanities course work. Project Gutenberg Finnish texts with topic modelling.

What does it do?
----------------

A small Python program that allows making similarity comparisons of arbitrary texts against the corpus of Project Gutenberg Finnish fulltexts.


Project Background
------------------

This project is a final assignment for Introduction to Digital Humanities -course I partook at the University of Helsinki in Autumn 2015.

The code is based on / blatantly copied from a topic modeling tutorial available at https://github.com/piskvorky/topic_modeling_tutorial . That tutorial is by Radim Řehůřek, the author of gensim. Gensim is a topic modeling library for Python, and the main tool employed here. NLTK is used for stemming of Finnish words.  

The code is horribly messy, and follows the structure of the aforementioned tutorial quite closely.

Sourcefile is a dump from Project Gutenberg database, 1246 literature fulltexts in Finnish. The directory structure has been flattened and encoding changed to utf-8. Files have not been otherwise altered. Project Gutenberg dumps are obtainable with methods specified here: http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages


Usage
-----
1. Create a Python 2.7 virtualenv
2. pip install requirements.txt
3. download sourcefile from https://www.hightail.com/download/ZWJXWmdveDNKV05MWE1UQw and save in gutenberparser/data/ -directory
4. Run pgfin_main_datagenerator.py to parse tarfile, and generate topics and indices, or run clean_and_savemm.py, pgfin_lsi_analysis.py, pgfin_index.py, in that order.
5. add a plaintext file to make queries agains the "database" created in previous step. The file should be placed in gutenbergparser/queryfiles/
6. modify and run pgfin_query.py to get query results. The default queryfile is queryfile.txt, a text found in the corpus.

Results from running pgfin_query.py should look something like this:
```
    Getting closest hits for queryfile: ./queryfiles/queryfile.txt ...

Dante: Jumalainen näytelmä: Helvetti (96%)
Dante: Jumalainen näytelmä: Kiirastuli (92%)
Dante: Jumalainen näytelmä I-III (90%)
Johann Wolfgang von Goethe: Runoelmia (87%)
Eino Leino: Juhana Herttuan ja Catharina Jagellonican lauluja (86%)
```


Further development?
--------------------

The state of the project is currently somewhere around proof-of-concept / alpha. Next steps in development would be:

* code rewrite & restructuring (messy & slow)
* creating a light webapp frontend for making queries


Thoughts
--------

The tool currently doesn't have a real use, but creating it served as a good way to learn basics of topic modeling in Python. The basic concept seems somewhat sound: a query with a text of Dante's return other texts by him as closest matches, so at least some similarity is reflected in the method. Further testing and refinement would of course be needed to actually verify the method.
