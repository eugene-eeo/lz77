import math
from bitarray import bitarray


EOF = object()


def find_longest_match(s, w, b, min_length=1):
    wl, wh = w
    bl, bh = b
    buffer = memoryview(s)[bl:bh]
    maxlen = min(bh - bl, bh - wl)
    D = 0
    L = 0
    lo = wl
    # go from l,l-1,l-2,...,1
    for l in range(min_length, maxlen + 1):
        lo = s.find(buffer[:l], lo, bh)
        if lo == -1 or lo >= wh:
            break
        L = l
        D = wh - lo
    return D, L


def encode_triplets(s, W, L):
    p = 0
    n = len(s)
    while p < n:
        window = (max(0, p-W), p)
        buffer = (p, min(p+L, n))
        d, l = find_longest_match(s, window, buffer)
        if p + l == n:
            c = EOF
        else:
            c = s[p+l]
        yield d, l, c
        p += l + 1


def bits_needed(x):
    return int(math.ceil(math.log2(x)))


def make_encoder(width):
    def encoder(n, fmt=("{n:0%db}" % width)):
        return fmt.format(n=n)
    return encoder


def deflate(s, W, L):
    encode_d = make_encoder(bits_needed(W + 1))
    encode_l = make_encoder(bits_needed(L + 1))
    encode_c = make_encoder(8)
    b = bitarray()
    for d, l, c in encode_triplets(s, W, L):
        b.extend(encode_d(d))
        b.extend(encode_l(l))
        if c is EOF:
            break
        b.extend(encode_c(c))
    return b


def inflate_to_tuples(b, W, L):
    n = bits_needed(W + 1)
    m = bits_needed(L + 1)
    i = 0
    B = len(b)
    while i < B:
        d = b[i:i+n].to01(); i += n  # distance
        l = b[i:i+m].to01(); i += m  # length
        c = b[i:i+8].to01(); i += 8  # char
        yield (
            int(d, base=2),
            int(l, base=2),
            int(c, base=2) if c else EOF,
        )


def inflate(b, W, L, method=inflate_to_tuples):
    o = bytearray()
    for d, l, c in method(b, W, L):
        if l != 0:
            w = o[-d:]
            while l > d:
                l -= d
                o.extend(w)
            o.extend(w[:l])
        if c is EOF:
            break
        o.append(c)
    return bytes(o)
