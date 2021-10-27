Sharique Shamim
2018CS10388
COL764: Assignment1

Directory Structure

2018CS10388
|_
   utils.py
   PorterStemmer.py
   invidx_cons.py
   boolsearch.py
   build.sh
   invidx.sh
   boolsearch.sh
   2018CS10388.pdf
   README.md

How to run the code?
Requirements: bs4, snappy

$ pip3 install bs4
$ pip3 install snappy
$ bash build.sh
$ bash invidx.sh coll-path indexfile stopwordfile {0|1|2|3|4|5} xml-tags-info
$ bash boolsearch.py queryfile resultfile indexfile dictfile

What will be printed console ?
For bash invidx.sh
1. Time to create inverted index
2. Compression Method
3. Time to compress inverted index

For boolsearch.sh
1. Decompression Method
2. Time to solve queries