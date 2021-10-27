import os
import sys
import time
from bs4 import BeautifulSoup
from utils import *

coll_path = sys.argv[1]
indexfile = sys.argv[2]
stopword_file = sys.argv[3]
strategy = int(sys.argv[4])
xml_tags_info = sys.argv[5]

DOC_NO = 0
INV_IDX_DICT = {}
INV_IDX = {}
CINV_IDX = {}

def insert_idx(filename, xml_tags, stopwords):
    global DOC_NO
    with open(filename, 'r', encoding='iso-8859-1') as f:
        soup = BeautifulSoup(f, 'html.parser')
    all_docs = soup.find_all('doc')
    for doc in all_docs:
        DOC_NO += 1
        doc_no = doc.find(xml_tags[0].lower()).text.strip()
        for tag in xml_tags[1:]:
            tag_doc = doc.find_all(tag.lower())
            if tag_doc == None: continue
            for tgd in tag_doc:
                stemmed_tag_text = getStemmedText(tgd.text, stopwords)
                for word in stemmed_tag_text:
                    if INV_IDX.get(word, None) is None:
                        INV_IDX[word] = {DOC_NO}
                    else:
                        INV_IDX[word].add(DOC_NO)
        INV_IDX_DICT[DOC_NO] = doc_no

def create_idx(docs_path, xml_tags, stopwords):
    doc_files = os.listdir(docs_path)
    for i in range(len(doc_files)):
        print('i = {}, file = {}'.format(i, doc_files[i]))
        filename = os.path.join(docs_path, doc_files[i])
        insert_idx(filename, xml_tags, stopwords)

def compress_idx(c):
    for term in INV_IDX:
        gap_pl = encode_gap(INV_IDX[term])
        CINV_IDX[term] = gap_pl if c == 0 else compress(gap_pl, c)

xml_tags = read_file(xml_tags_info)
stopwords = read_file(stopword_file)

start = time.time()
create_idx(coll_path, xml_tags, stopwords)
end = time.time()
print('Time to create Inverted Index = {} seconds'.format(end-start))

INV_IDX_DICT['stopwords'] = stopwords
INV_IDX_DICT['METHOD'] = strategy
print('Compression Method : c{}'.format(strategy))

start = time.time()
compress_idx(strategy)
end = time.time()
print('Time to compress Inverted Index = {} seconds'.format(end-start))

write_pickle(indexfile + '.dict', INV_IDX_DICT)
write_pickle(indexfile + '.idx', CINV_IDX)