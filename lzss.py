import math
from bitarray import bitarray
from functools import partial
from lz77 import bits_needed, find_longest_match, EOF, make_encoder, inflate


def encode_triplets(s, W, L):
    break_even = bits_needed(W + 1)
    window = b""
    while s:
        buffer = s[:L]
        d, l = find_longest_match(window, buffer)
        if d > 0:
            if l <= break_even:
                for i in range(l):
                    yield 0, 0, s[i]
                window = (window + s[:l])[-W:]
                s = s[l:]
                continue
            c = s[l] if len(s) > l else EOF
        else:
            c = s[0]

        yield d, l, c
        window = (window + s[:l+1])[-W:]
        s = s[l+1:]


def deflate(s, W, L):
    encode_i = make_encoder(bits_needed(W + 1))
    encode_d = make_encoder(bits_needed(L + 1))
    encode_c = make_encoder(8)
    b = bitarray()
    for i, d, c in encode_triplets(s, W, L):
        is_char = i == 0 and d == 0
        b.extend([is_char])
        if is_char:
            # we never ever get is_char == True if c is an EOF.
            # c is only ever EOF if the last sequence can be found
            # in the sliding window.
            b.extend(encode_c(c))
        else:
            b.extend(encode_i(i))
            b.extend(encode_d(d))
            if c is EOF:
                break
            b.extend(encode_c(c))
    return b


def inflate_to_tuples(b, W, L):
    n = bits_needed(W + 1)
    m = bits_needed(L + 1)
    p = 0
    l = len(b)
    while p < l:
        is_char = b[p]; p += 1 # is_char
        if is_char:
            c = b[p:p+8].to01(); p += 8
            yield 0, 0, int(c, base=2)
        else:
            i = b[p:p+n].to01(); p += n  # pos
            d = b[p:p+m].to01(); p += m  # length
            c = b[p:p+8].to01(); p += 8  # char
            yield (
                int(i, base=2),
                int(d, base=2),
                int(c, base=2) if c else EOF,
            )


inflate = partial(inflate, method=inflate_to_tuples)
