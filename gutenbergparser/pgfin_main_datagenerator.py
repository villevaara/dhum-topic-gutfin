print "\n    Generating tokens and metadata from tarfile. \n" \
      "    Running clean_and_savemm.py - this might take a bit less than 30 mins.\n"

import clean_and_savemm

print "\n    Performing lsi analysis. \n" \
      "    Running pgfin_lsi_analysis.py - This will taka a good while too.\n"

import pgfin_lsi_analysis

print "\n    Building indices. \n" \
      "    Running pgfin_index.py - Just takes a minute. \n"

import pgfin_index

print "\n    Modify queryfile -variable in pgfin_query.py\n" \
      "    and run it to test database.\n"