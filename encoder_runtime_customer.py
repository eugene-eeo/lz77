import csv
import time
from lz77 import deflate, inflate

P = [0.1 * i for i in range(1, 11)]
W = [2**i-1 for i in [16]]
L = [2**i-1 for i in [8]]

pairs = [
    ['corpus/customer.xml', 'results/customer.csv'],
    ['corpus/bible.txt', 'results/bible.csv'],
    ['corpus/image.jpg', 'results/image.csv'],
    ['corpus/zeros.txt', 'results/zeros.csv'],
]

for input_file, results_file in pairs:
    b = open(input_file, mode="rb").read()
    N = len(b)
    out = csv.writer(open(results_file, mode="w"))
    out.writerow(["Percentage", "W", "L", "Compression Ratio", "Encode Time", "Decode Time"])

    for w in W:
        for l in L:
            for p in P:
                print("{input_file} {w} {l} {p:.2f}".format(input_file=input_file, p=p, w=w, l=l))
                buff = b[:int(p*N)]
                deflate_t0 = time.time()
                x = deflate(buff, W=w, L=l)
                deflate_t1 = time.time()
                inflate_t0 = time.time()
                inflate(x, W=w, L=l)
                inflate_t1 = time.time()
                x.fill()
                out.writerow([
                    p,
                    w,
                    l,
                    (len(x) // 8) / len(b),
                    deflate_t1 - deflate_t0,
                    inflate_t1 - inflate_t0,
                ])
