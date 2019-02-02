import csv
from time import time
from lzss import inflate, deflate

pairs = [
    #['corpus/customer.xml', 'results/lzss-customer.csv'],
    #['corpus/bible.txt',    'results/lzss-bible.csv'],
    ['corpus/image.jpg',    'results/lzss-image.csv'],
    #['corpus/zeros.txt',    'results/lzss-zeros.csv'],
]


W = [2**i-1 for i in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]]
L = [2**i-1 for i in [8]]


for input_file, results_file in pairs:
    b = open(input_file, mode="rb").read()
    out = csv.writer(open(results_file, mode="w"))
    out.writerow(["W", "L", "Compression Ratio", "Encode Time", "Decode Time"])

    for w in W:
        for l in L:
            print("{input_file} {w} {l}".format(input_file=input_file, w=w, l=l))
            deflate_t0 = time()
            x = deflate(b, W=w, L=l)
            deflate_t1 = time()
            inflate_t0 = time()
            inflate(x, W=w, L=l)
            inflate_t1 = time()
            x.fill()
            out.writerow([
                w,
                l,
                (len(x) // 8) / len(b),
                deflate_t1 - deflate_t0,
                inflate_t1 - inflate_t0,
            ])
