import math
from bitarray import bitarray
from functools import partial
from lz77 import bits_needed, encode_triplets, EOF, encode_int, inflate


def deflate(s, W, L):
    n = bits_needed(W)
    m = bits_needed(L)
    b = bitarray()
    for i, d, c in encode_triplets(s, W, L):
        is_char = i == 0 and d == 0
        b.extend([is_char])
        if is_char:
            # we never ever get is_char == True if c is an EOF.
            # c is only ever EOF if the last sequence can be found
            # in the sliding window.
            b.extend(encode_int(c, 8))
        else:
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
        is_char = b[p]; p += 1 # is_char
        if is_char:
            c = b[p:p+8].to01(); p += 8
            yield (0, 0, chr(int(c, base=2)).encode('ascii'))
            continue

        i = b[p:p+n].to01(); p += n  # pos
        d = b[p:p+m].to01(); p += m  # length
        c = b[p:p+8].to01(); p += 8  # char
        yield (
            int(i, base=2),
            int(d, base=2),
            chr(int(c, base=2)).encode('ascii') if c else EOF,
        )


inflate = partial(inflate, method=inflate_to_tuples)
