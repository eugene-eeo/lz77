import csv
import lz77
import lzss
import lzw


deflate = lambda b, W, L: lzw.encode(b, W)


impls = [
    ['lz77-', lz77.deflate],
    ['lzss-', lzss.deflate],
    ['lzw-',  deflate],
]

W = [2**i-1 for i in [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32]]
L = [2**i-1 for i in [8]]
b = open("corpus/genesis.txt", mode="rb").read()


for prefix, deflate in impls:
    out = csv.writer(open("results/" + prefix + "genesis.csv", mode="w"))
    out.writerow(["W", "L", "Compression Ratio"])
    for w in W:
        for l in L:
            print(prefix, w, l)
            x = deflate(b, W=w, L=l)
            x.fill()
            out.writerow([
                w,
                l,
                (len(x) // 8) / len(b),
            ])
