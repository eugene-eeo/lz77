import csv
from time import time
from lzw import decode, encode

pairs = [
    ['corpus/bible.txt',    'results/lzw-bible.csv'],
    ['corpus/image.jpg',    'results/lzw-image.csv'],
]


W = [2**i for i in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]]


for input_file, results_file in pairs:
    b = open(input_file, mode="rb").read()
    out = csv.writer(open(results_file, mode="w"))
    out.writerow(["W", "Encode Time", "Decode Time"])

    for w in W:
        print("{input_file} {w}".format(input_file=input_file, w=w))
        total_deflate = 0
        total_inflate = 0

        for i in range(10):
            print(i)
            deflate_t0 = time()
            x = encode(b, w)
            deflate_t1 = time()
            inflate_t0 = time()
            decode(x, w)
            inflate_t1 = time()

            total_deflate += deflate_t1 - deflate_t0
            total_inflate += inflate_t1 - inflate_t0

        out.writerow([
            w,
            total_deflate / 10.0,
            total_inflate / 10.0,
        ])
