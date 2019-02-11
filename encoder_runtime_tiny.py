import csv
import time
from lz77 import deflate, inflate

W = [1, 15, 63, 255]
L = 255
n = 10000

out = csv.writer(open("results/tiny.csv", mode="w"))
out.writerow(["n-rep", "W", "Compression Ratio", "Encode Time", "Decode Time"])

for nrep, name in [
        [256, "tiny-zero"],
        [128, "tiny-2"],
        [64,  "tiny-4"],
        [32,  "tiny-8"],
        [16,  "tiny-16"],
        [8,   "tiny-32"],
        [4,   "tiny-64"],
        [2,   "tiny-128"],
        [1,   "uniq"],
        ]:
    b = open(f"corpus/{name}.txt", mode="rb").read()
    print(nrep, name)
    for w in W:
        deflate_total = 0
        inflate_total = 0
        for i in range(n):
            deflate_t0 = time.time()
            x = deflate(b, w, L)
            deflate_t1 = time.time()
            inflate_t0 = time.time()
            inflate(x, w, L)
            inflate_t1 = time.time()
            deflate_total += deflate_t1 - deflate_t0
            inflate_total += inflate_t1 - inflate_t0
        x.fill()
        out.writerow([
            nrep,
            w,
            (len(x) // 8) / len(b),
            deflate_total / n,
            inflate_total / n,
        ])
