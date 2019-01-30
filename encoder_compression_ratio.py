import csv
import time
from lz77 import deflate, inflate

W = [2**i-1 for i in [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]]
L = [2**i-1 for i in [8]]
b = open("corpus/genesis.txt", mode="rb").read()
out = csv.writer(open("results/genesis.csv", mode="w"))
out.writerow(["W", "L", "Compression Ratio", "Encode Time", "Decode Time"])

for w in W:
    for l in L:
        print(w, l)
        deflate_t0 = time.time()
        x = deflate(b, W=w, L=l)
        deflate_t1 = time.time()
        inflate_t0 = time.time()
        inflate(x, W=w, L=l)
        inflate_t1 = time.time()
        x.fill()
        out.writerow([
            w,
            l,
            (len(x) // 8) / len(b),
            deflate_t1 - deflate_t0,
            inflate_t1 - inflate_t0,
        ])
