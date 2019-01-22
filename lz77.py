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


def bits_needed(x):
    return int(math.ceil(math.log2(1 + x)))


def encode_int(n, width):
    return "{n:0{width}b}".format(n=n, width=width)


def deflate(s, W, L):
    n = bits_needed(W)
    m = bits_needed(L)
    b = bitarray()
    for i, d, c in encode_triplets(s, W, L):
        b.extend(encode_int(i, n))
        b.extend(encode_int(d, m))
        if c is EOF:
            break
        b.extend(encode_int(c, 8))
    return b


def inflate_to_tuples(b, W, L):
    n = bits_needed(W)
    m = bits_needed(L)
    p = 0
    l = len(b)
    while p < l:
        i = b[p:p+n].to01(); p += n  # pos
        d = b[p:p+m].to01(); p += m  # length
        c = b[p:p+8].to01(); p += 8  # char
        yield (
            int(i, base=2),
            int(d, base=2),
            chr(int(c, base=2)).encode('ascii') if c else EOF,
        )


def inflate(b, W, L, method=inflate_to_tuples):
    length = 0
    output = b""
    for i, d, c in method(b, W, L):
        pos = length - i
        output += output[pos:pos+d]
        length += d
        if c is EOF:
            break
        output += c
        length += 1
    return output
