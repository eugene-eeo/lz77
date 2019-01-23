import csv
import time
from lz77 import deflate, inflate

W = [50*i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
L = [50*i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
buf = open("corpus/beers.txt", mode="rb").read().splitlines()
out = csv.writer(open("results/beers.csv", mode="w"))
out.writerow(["W", "L", "Lines", "Compression Ratio", "Encode Time", "Decode Time"])

for w in W:
    for l in L:
        print(w, l)
        for i in range(0, 101, 2):
            if i == 0:
                continue
            b = b"\n".join(buf[:2*i])
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
                i,
                (len(x) // 8) / len(b),
                deflate_t1 - deflate_t0,
                inflate_t1 - inflate_t0,
            ])
