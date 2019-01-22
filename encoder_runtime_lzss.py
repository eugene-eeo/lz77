import sys
import json
import time
from lzss import inflate, deflate


for filename in [
        "corpus/mini-beers.txt",
        "corpus/mini-names.txt",
        "corpus/beers.txt",
        "corpus/names.txt",
        ]:
    buff = open(filename, "rb").read()
    for W in [15, 63, 255, 1023, 4095, 65535]:
        for L in [15, 31, 63, 127, 255, 511]:
            print(filename, W, L, file=sys.stderr)
            for i in range(100):
                deflate_t0 = time.time()
                x = deflate(buff, W=W, L=L)
                deflate_t1 = time.time()
                inflate_t0 = time.time()
                inflate(x, W=W, L=L)
                inflate_t1 = time.time()
                x.fill()
                print(json.dumps([
                    filename,                  # filename
                    W,                         # W
                    L,                         # L
                    (len(x) // 8) / len(buff), # compression ratio
                    deflate_t1 - deflate_t0,   # deflate/encode time
                    inflate_t1 - inflate_t0,   # inflate/decode time
                ]))
