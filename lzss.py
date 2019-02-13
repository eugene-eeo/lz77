import math
from bitarray import bitarray
from functools import partial
from lz77 import bits_needed, find_longest_match, EOF, make_encoder, inflate


def encode_triplets(s, W, L):
    break_even = (bits_needed(W + 1) + bits_needed(L + 1)) // 8 + 1
    p = 0
    n = len(s)
    while p < n:
        window = (max(0, p-W), p)
        buffer = (p, min(p+L, n))
        d, l = find_longest_match(s, window, buffer, break_even)
        if p + l == n:
            c = EOF
        else:
            c = s[p+l]
        yield d, l, c
        p += l + 1


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
    i = 0
    B = len(b)
    N = B - n - m
    while i < B:
        is_char = b[i]; i += 1 # is_char
        if is_char:
            c = b[i:i+8].to01(); i += 8
            yield 0, 0, int(c, base=2)
        else:
            if i > N:
                return
            d = b[i:i+n].to01(); i += n  # pos
            l = b[i:i+m].to01(); i += m  # length
            c = b[i:i+8].to01(); i += 8  # char
            yield (
                int(d, base=2),
                int(l, base=2),
                int(c, base=2) if i <= B else EOF,
            )


inflate = partial(inflate, method=inflate_to_tuples)
