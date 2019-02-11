from bitarray import bitarray
from lz77 import make_encoder, bits_needed


def to_indices(data, max_length):
    if len(data) == 0:
        return

    s = b""
    d = {bytes([i]): i for i in range(256)}
    m = 8
    size = 2**m
    stop = max_length == 256

    for ch in data:
        ch = bytes([ch])
        if s + ch in d:
            s += ch
        else:
            if not stop:
                if len(d) == size:
                    m += 1
                    size *= 2
                d[s+ch] = len(d)
                stop = len(d) == max_length
            yield d[s], m
            s = ch
    yield d[s], m


def encode(data, max_length=4096):
    m = 8
    e = make_encoder(8)
    b = bitarray()
    for x, bits in to_indices(data, max_length):
        if bits != m:
            m = bits
            e = make_encoder(bits)
        b.extend(e(x))
    return b


def get_next_code(data, p, m):
    curr = int(data[p:p+m].to01(), base=2)
    p += m
    return curr, p


def decode(data, max_length):
    n = len(data)
    p = 0
    m = 8 if max_length == 256 else 9
    d = {i: bytes([i]) for i in range(256)}
    o = bytearray()
    w = b""

    c, p = get_next_code(data, p, m)
    w = d[c]
    o.extend(w)

    size = 2**m
    d_size = 256

    while p < n:
        # if we need to increase the size of the dictionary and
        # we can (max length bound) then m++
        if d_size+1 == size and d_size+1 < max_length:
            size *= 2
            m += 1
        code, p = get_next_code(data, p, m)
        if code in d:
            t = w
            w = d[code]
            d[d_size] = t + w[:1]
        else:
            d[d_size] = w + w[:1]
            w = d[code]
        o.extend(w)
        d_size += 1
    return bytes(o)
