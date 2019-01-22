import json
import time
from lz77 import inflate, deflate


for filename in [
        #"corpus/mini-beers.txt",
        "corpus/mini-names.txt",
        "corpus/beers.txt",
        "corpus/names.txt",
        ]:
    buff = open(filename, "rb").read()
    for L in [15, 31, 63, 127, 255, 511]:
        for W in [255, 511, 1023, 2047, 4095, 65535]:
            for i in range(100):
                deflate_t0 = time.time()
                x = deflate(buff, W, L)
                deflate_t1 = time.time()
                inflate_t0 = time.time()
                inflate(x, W, L)
                inflate_t1 = time.time()
                print(json.dumps([
                    filename,                  # filename
                    L,                         # L
                    W,                         # W
                    len(x) / len(buff),        # compression ratio
                    deflate_t1 - deflate_t0,   # deflate/encode time
                    inflate_t1 - inflate_t0,   # inflate/decode time
                ]))
