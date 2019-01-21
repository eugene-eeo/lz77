import math
from bitarray import bitarray


EOF = object()


def find_longest_prefix(buffer, window):
    for i in range(len(buffer), 0, -1):
        x = window.rfind(buffer[:i])
        if x != -1:
            return i, x
    return None, -1


def keep_last_n(s, n):
    m = len(s)
    return s[m-n:m]


def encode_triplets(s, W, L):
    window = b''
    while s:
        buffer = s[:L]
        length, pos = find_longest_prefix(buffer, window)
        if length is not None:
            i = len(window) - pos
            d = length
            c = s[d] if len(s) > d else EOF
        else:
            i = 0
            d = 0
            c = s[0]

        yield (i, d, c)

        # pop and maintain window
        p = s[0:d+1]
        s = s[d+1:]
        window = keep_last_n(window + p, W)


def encode_int(n, N):
    x = bin(n)[2:]
    return bitarray(('0' * (N - len(x))) + x)


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
        i = b[:n]; b = b[n:] # pos
        d = b[:m]; b = b[m:] # length
        c = b[:8]; b = b[8:] # char
        i = int(i.to01(), base=2)
        d = int(d.to01(), base=2)
        c = (chr(int(c.to01(), base=2)).encode('ascii') if len(c) > 0 else
             EOF)
        yield i, d, c


def inflate(b, W, L):
    output = b""
    for i, d, c in inflate_to_tuples(b, W, L):
        pos = len(output) - i
        output += output[pos:pos+d]
        if c is EOF:
            break
        output += c
    return output
