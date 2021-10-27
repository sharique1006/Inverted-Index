import os
import sys
import time
from utils import *

queryfile = sys.argv[1]
resultfile = sys.argv[2]
indexfile = sys.argv[3]
dictfile = sys.argv[4] 

INV_IDX_DICT = read_pickle(dictfile)
INV_IDX = read_pickle(indexfile)

def solve_queries(queries, stopwords, c):
    results = []
    for i in range(len(queries)):
        all_stemmed_q = getStemmedText(queries[i], stopwords)
        stemmed_q = []
        for x in all_stemmed_q:
            if x in INV_IDX:
                stemmed_q += [x]

        if len(stemmed_q) == 0:
            results += ['Q'+str(i)+'   1.0']
            continue
        curr = decode_gap(decompress(INV_IDX[stemmed_q[0]], c))
        docs = set([INV_IDX_DICT[x] for x in curr])
        for j in range(1, len(stemmed_q)):
            curr = decode_gap(decompress(INV_IDX[stemmed_q[j]], c))
            mapped_curr = set([INV_IDX_DICT[x] for x in curr])
            docs.intersection_update(mapped_curr)
        # res = ' '.join([str(x) for x in sorted(docs)])
        # results += ['Q'+str(i)+' '+res+' 1.0']
        res = ['Q'+str(i)+' '+str(x)+' 1.0' for x in sorted(docs)]
        results += res
    return results

queries = read_file(queryfile)
stopwords = INV_IDX_DICT['stopwords']
strategy = INV_IDX_DICT['METHOD']
print('Decompression Method : c{}'.format(strategy))

start = time.time()
results = solve_queries(queries, stopwords, strategy)
end = time.time()
print('Average Time taken per query = {} seconds'.format((end-start)/len(queries)))

write_file(resultfile, results)

