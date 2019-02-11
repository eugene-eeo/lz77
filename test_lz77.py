import pytest
import lz77
import lzss
import lzw


abracadabra = "abracadabra"
shell = (
    "She sells seashells by the seashore. "
    "The shells she sells are surely seashells. "
    "So if she sells shells on the seashore, "
    "I'm sure she sells seashore shells."
    )
peter = (
    'Peter Piper picked a peck of pickled peppers. '
    'A peck of pickled peppers Peter Piper picked. '
    'If Peter Piper picked a peck of pickled peppers, '
    "where's the peck of pickled peppers Peter Piper picked?"
    )
text = (
    'Unique New York. '
    'Many an anemone sees an enemy anemone. '
    'Freshly-fried flying fish. '
    'She stood on the balcony, '
    'inexplicably mimicking him hiccoughing, '
    'and amicably welcoming him home. '
    'Imagine an imaginary menagerie manager '
    'imagining managing an imaginary menagerie. '
    'The epitome of femininity. '
    'A skunk sat on a stump and thunk the stump stunk, '
    'but the stump thunk the skunk stunk. '
    'Greek grapes.'
    )


corpus = [abracadabra, peter, shell, text]


@pytest.mark.parametrize("impl", [lz77, lzss])
@pytest.mark.parametrize("x", corpus)
@pytest.mark.parametrize("W", [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 100, 127, 255, 511])
@pytest.mark.parametrize("L", [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 100, 127, 255, 511])
def test_inflate_deflate(impl, x, W, L):
    b = x.encode('ascii')
    assert impl.inflate(impl.deflate(b, W, L), W, L) == b


@pytest.mark.parametrize("impl", [lz77, lzss])
@pytest.mark.parametrize("x", corpus)
def test_inflate_deflate_lz77_values(impl, x):
    test_inflate_deflate(impl, x, 65535, 255)


@pytest.mark.parametrize("impl", [lz77, lzss])
@pytest.mark.parametrize("b", [
    open("corpus/mini-beers.txt", "rb").read(),
    open("corpus/mini-names.txt", "rb").read(),
    open("corpus/beers.txt", "rb").read(),
    open("corpus/names.txt", "rb").read(),
    ])
def test_inflate_deflate_corpus(impl, b, W=255, L=255):
    assert impl.inflate(impl.deflate(b, W, L), W, L) == b


@pytest.mark.parametrize("W", [2**i for i in range(8, 33)])
@pytest.mark.parametrize("x", corpus + [
    open("corpus/mini-beers.txt", "rb").read(),
    open("corpus/mini-names.txt", "rb").read(),
    open("corpus/beers.txt", "rb").read(),
    open("corpus/names.txt", "rb").read(),
    ])
def test_lzw(x, W):
    b = x
    if hasattr(x, 'encode'):
        b = x.encode("ascii")
    assert lzw.decode(lzw.encode(b, W), W) == b


def test_encode_triplets():
    assert [(d,l,chr(c)) for d,l,c in lz77.encode_triplets(b"aacaacabcabaaac", 6, 4)] == [
            (0, 0, 'a'),
            (1, 1, 'c'),
            (3, 4, 'b'),
            (3, 3, 'a'),
            (1, 2, 'c'),
        ]
