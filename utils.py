import re
import math
import snappy
import _pickle as cPickle
from functools import lru_cache
from struct import pack, unpack
from PorterStemmer import *

def read_file(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()
    return data

def write_file(filename, data):
    with open(filename, 'w') as f:
        for d in data:
            f.write(d + '\n')

def read_pickle(filename):
    with open(filename, 'rb') as f:
        data = cPickle.load(f)
    return data

def write_pickle(filename, data):
    with open(filename, 'wb') as f:
        cPickle.dump(data, f)

def getStemmedText(text, stopwords):
    ps = PorterStemmer()
    p_stemmer = lru_cache(maxsize=None)(ps.stem)
    tokens = re.split(r"[ ?_!~(){}`'\",;:.\n]+", text)
    tokens = filter(lambda token: token not in stopwords and (token.isupper() or len(token)>3), tokens)
    stemmed_tokens = map(lambda token: p_stemmer(token, 0, len(token)-1), tokens)
    return list(stemmed_tokens)

def encode_gap(pl):
    pl = sorted(list(pl))
    gap_pl = [pl[0]]
    for i in range(1, len(pl)):
        gap_pl += [pl[i] - pl[i-1]]
    return gap_pl

def decode_gap(gap_pl):
    pl = [gap_pl[0]]
    for i in range(1, len(gap_pl)):
        pl += [gap_pl[i] + pl[-1]]
    return pl

def compress_1(nlist):
    def helper(n):
        bl = []
        while True:
            bl.insert(0, n % 128)
            if n < 128:
                break
            n = n // 128
        bl[-1] += 128
        return pack('%dB' % len(bl), *bl)
    bytes_list = []
    for n in nlist:
        bytes_list.append(helper(n))
    return b"".join(bytes_list)

def decompress_1(bytestream):
    n = 0
    nlist = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            nlist.append(n)
            n = 0
    return nlist

def compress_2(nlist):
    def helper(n):
        L = math.floor(math.log(n, 2))
        R = math.floor(math.log(L+1, 2))
        return [R, L+1, n]
    delta = []
    for n in nlist:
        delta += helper(n)
    return compress_1(delta)

def decompress_2(bytestream):
    def helper(a, b, c):
        if c ==  1: return 1
        s = '0'*a + bin(b)[2:] + bin(c)[2:][1-b:]
        L = len(s.split('1')[0])
        R = int(s[:2*L+1], 2) - 1
        r = int(s[-R:], 2)
        return 2**R+r
    curr = decompress_1(bytestream)
    nlist = []
    for i in range(2, len(curr), 3):
        n = helper(curr[i-2], curr[i-1], curr[i])
        nlist.append(n)
    return nlist

def compress_3(nlist):
    a = [str(n) for n in nlist]
    return snappy.compress(' '.join(a))

def decompress_3(bytestream):
    bytes_list = snappy.uncompress(bytestream)
    s = bytes_list.decode('utf-8').split(' ')
    nlist = [int(n) for n in s]
    return nlist

def compress_4(nlist):
    def helper(n):
        k = math.floor(math.log(n, 2))
        q = n // 2**k
        r = n - q*(2**k)
        return [q, k, r]
    golomb = []
    for n in nlist:
        golomb += helper(n)
    return compress_1(golomb)

def decompress_4(bytestream):        
    curr = decompress_1(bytestream)
    nlist = []
    for i in range(2, len(curr), 3):
        n = curr[i-2]*(2**curr[i-1]) + curr[i]
        nlist.append(n)
    return nlist

def compress(nlist, c):
    if c == 1: return compress_1(nlist)
    if c == 2: return compress_2(nlist)
    if c == 3: return compress_3(nlist)
    if c == 4: return compress_4(nlist)
    if c == 5: return compress_1(nlist)
    return nlist

def decompress(bytestream, c):
    if c == 1: return decompress_1(bytestream)
    if c == 2: return decompress_2(bytestream)
    if c == 3: return decompress_3(bytestream)
    if c == 4: return decompress_4(bytestream)
    if c == 5: return decompress_1(bytestream)
    return bytestream