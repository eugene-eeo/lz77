from bitarray import bitarray
from lz77 import make_encoder, bits_needed


def to_indices(data, max_length):
    if len(data) == 0:
        return

    s = b""
    d = {bytes([i]): i for i in range(256)}

    for ch in data:
        ch = bytes([ch])
        if s + ch in d:
            s += ch
        else:
            yield d[s]
            if len(d) < max_length:
                d[s+ch] = len(d)
            s = ch
    yield d[s]


def encode(data, max_length=4096):
    e = make_encoder(bits_needed(max_length))
    b = bitarray()
    for x in to_indices(data, max_length):
        b.extend(e(x))
    return b


def inflate_to_indices(data, max_length):
    m = bits_needed(max_length)
    p = 0
    n = len(data)
    while p < n:
        curr = int(data[p:p+m].to01(), base=2)
        p += m
        yield curr


def decode(data, max_length=4096):
    codes = inflate_to_indices(data, max_length)
    output = b""

    d = {i: bytes([i]) for i in range(256)}
    t = b""
    w = b""

    w = d[next(codes)]
    output += w

    for code in codes:
        if code in d:
            t = w
            w = d[code]
            d[len(d)] = t + w[:1]
        else:
            d[len(d)] = w + w[:1]
            w = d[code]
        output += w

    return output
