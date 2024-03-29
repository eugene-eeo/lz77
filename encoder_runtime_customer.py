import csv
import time
from lz77 import deflate, inflate

# W => [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

P = [0.1 * i for i in range(1, 11)]
W = [2**i-1 for i in [16]]
L = [2**i-1 for i in [8]]

pairs = [
    ['corpus/customer.xml', 'results/lz77-runtime-customer.csv'],
    ['corpus/bible.txt', 'results/lz77-runtime-bible.csv'],
    ['corpus/image.jpg', 'results/lz77-runtime-image.csv'],
    ['corpus/zeros.txt', 'results/lz77-runtime-zeros.csv'],
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
