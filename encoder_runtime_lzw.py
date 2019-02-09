import csv
from time import time
from lzw import decode, encode

pairs = [
    ['corpus/customer.xml', 'results/lzw-customer.csv'],
    ['corpus/bible.txt',    'results/lzw-bible.csv'],
    ['corpus/image.jpg',    'results/lzw-image.csv'],
    ['corpus/zeros.txt',    'results/lzw-zeros.csv'],
]


W = [2**i for i in [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]]


for input_file, results_file in pairs:
    b = open(input_file, mode="rb").read()
    out = csv.writer(open(results_file, mode="w"))
    out.writerow(["W", "Compression Ratio", "Encode Time", "Decode Time"])

    for w in W:
        print("{input_file} {w}".format(input_file=input_file, w=w))
        deflate_t0 = time()
        x = encode(b, w)
        deflate_t1 = time()
        inflate_t0 = time()
        decode(x, w)
        inflate_t1 = time()
        x.fill()
        out.writerow([
            w,
            (len(x) // 8) / len(b),
            deflate_t1 - deflate_t0,
            inflate_t1 - inflate_t0,
        ])
