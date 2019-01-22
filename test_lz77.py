import pytest
import lz77
import lzss


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


@pytest.mark.parametrize("impl", [lz77, lzss])
@pytest.mark.parametrize("x", [abracadabra, peter, shell, text])
@pytest.mark.parametrize("W", [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 100, 127, 255, 511])
@pytest.mark.parametrize("L", [1, 2, 3, 4, 5, 10, 15, 20, 25, 30, 100, 127, 255, 511])
def test_inflate_deflate(impl, x, W, L):
    b = x.encode('ascii')
    assert impl.inflate(impl.deflate(b, W, L), W, L) == b


@pytest.mark.parametrize("impl", [lz77, lzss])
@pytest.mark.parametrize("x", [abracadabra, peter, shell, text])
def test_inflate_deflate_lz77_values(impl, x, W=65535, L=255):
    test_inflate_deflate(impl, x, W, L)
