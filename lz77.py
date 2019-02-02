import math
from bitarray import bitarray


EOF = object()


def find_longest_prefix(b, buff, wind, min_length=1):
    bl, bh = buff
    wl, wh = wind
    buffer = memoryview(b)[bl:bh]
    maxlen = min(bh - bl, wh - wl)
    lo = wl
    for l in range(min_length, maxlen+1):
        x = b.find(buffer[:l], lo, wh)
        if x == -1:
            if l == min_length:
                break
            return l-1, b.rfind(buffer[:l-1], lo, wh) - wl
        lo = x
    else:
        return maxlen, b.rfind(buffer[:maxlen], lo, wh) - wl
    return None, 0


def encode_triplets(s, W, L):
    p = 0
    n = len(s)
    while p < n:
        window = (max(p - W, 0), p)
        buffer = (p, min(p + L, n))
        length, pos = find_longest_prefix(s, buffer, window)
        if length is not None:
            wl, wh = window
            i = wh - wl - pos
            d = length
            c = s[p+d] if p+d < n else EOF
        else:
            i = 0
            d = 0
            c = s[p]

        yield (i, d, c)
        p += d + 1


def bits_needed(x):
    return int(math.ceil(math.log2(1 + x)))


def make_encoder(width):
    def encoder(n, fmt=("{n:0%db}" % width)):
        return fmt.format(n=n)
    return encoder


def deflate(s, W, L):
    encode_i = make_encoder(bits_needed(W))
    encode_d = make_encoder(bits_needed(L))
    encode_c = make_encoder(8)
    b = bitarray()
    for i, d, c in encode_triplets(s, W, L):
        b.extend(encode_i(i))
        b.extend(encode_d(d))
        if c is EOF:
            break
        b.extend(encode_c(c))
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
            int(c, base=2) if c else EOF,
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
        output += bytes([c])
        length += 1
    return output
