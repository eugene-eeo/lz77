import math
from bitarray import bitarray


EOF = object()


def find_longest_prefix(buffer, window):
    for i in range(len(buffer), 0, -1):
        x = window.rfind(buffer[:i])
        if x != -1:
            return i, x
    return None, -1


def encode_triplets(s, W, L):
    p = 0
    n = len(s)
    while p < n:
        window = s[max(p-W,0):p]
        buffer = s[p:p+L]
        length, pos = find_longest_prefix(buffer, window)
        if length is not None:
            i = len(window) - pos
            d = length
            c = s[p+d] if len(s) > p+d else EOF
        else:
            i = 0
            d = 0
            c = s[p]

        yield (i, d, c)
        p += d + 1


def encode_int(n, width):
    return "{n:0{width}b}".format(n=n, width=width)


def lz77(s, W, L):
    n = int(math.ceil(math.log2(1 + W)))
    m = int(math.ceil(math.log2(1 + L)))
    b = bitarray()
    for i, d, c in encode_triplets(s, W, L):
        b.extend(encode_int(i, n))
        b.extend(encode_int(d, m))
        if c is EOF:
            break
        b.extend(encode_int(c, 8))
    return b


def inflate_to_tuples(b, W, L):
    n = int(math.ceil(math.log2(1 + W)))
    m = int(math.ceil(math.log2(1 + L)))
    while b:
        i, b = b[:n].to01(), b[n:] # pos
        d, b = b[:m].to01(), b[m:] # length
        c, b = b[:8].to01(), b[8:] # char
        yield (
            int(i, base=2),
            int(d, base=2),
            chr(int(c, base=2)).encode('ascii') if c else EOF,
        )


def inflate(b, W, L):
    output = b""
    for i, d, c in inflate_to_tuples(b, W, L):
        pos = len(output) - i
        output += output[pos:pos+d]
        if c is EOF:
            break
        output += c
    return output
