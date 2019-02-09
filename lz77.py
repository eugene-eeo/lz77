import math
from bitarray import bitarray


EOF = object()


def find_longest_match(w, b):
    u = w + b
    # go from l,l-1,l-2,...,1
    for l in range(len(b), 0, -1):
        i = u.find(b[:l])
        if i != -1 and i < len(w):
            return len(w) - i, l
    return 0, 0


def encode_triplets(s, W, L):
    window = b""
    while s:
        buffer = s[:L]
        d, l = find_longest_match(window, buffer)
        if d > 0:
            c = s[l] if len(s) > l else EOF
        else:
            c = s[0]

        yield d, l, c
        window = (window + s[:l+1])[-W:]
        s = s[l+1:]


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
    o = bytearray([])
    for d, l, c in method(b, W, L):
        p = len(o) - d
        if l > d:
            w = o[-d:]
            k = l
            i = 0
            while k > 0:
                o.append(w[i])
                k -= 1
                i += 1
                i %= d
        else:
            o.extend(o[p:p+l])
        if c is EOF:
            break
        o.append(c)
    return bytes(o)
