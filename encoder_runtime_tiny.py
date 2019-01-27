import csv
import time
from lz77 import deflate, inflate

W = [31, 63, 127, 255]
L = 255
n = 100

out = csv.writer(open("results/tiny.csv", mode="w"))
out.writerow(["Name", "W", "Compression Ratio", "Encode Time", "Decode Time"])

for name in [
        "tiny-zero",
        "tiny-2",
        "tiny-4",
        "tiny-8",
        "tiny-16",
        "tiny-32",
        "tiny-64",
        "tiny-128",
        "uniq",
        ]:
    b = open(f"corpus/{name}.txt", mode="rb").read()
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
            name,
            w,
            (len(x) // 8) / len(b),
            deflate_total / n,
            inflate_total / n,
        ])
