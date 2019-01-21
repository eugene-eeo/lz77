import pytest
from lz77 import inflate, lz77


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


@pytest.mark.parametrize("x", [abracadabra, peter, shell])
@pytest.mark.parametrize("W", [1, 2, 3, 4, 5, 10, 15, 100])
@pytest.mark.parametrize("L", [1, 2, 3, 4, 5, 10, 15, 100])
def test_inflate_deflate(x, W, L):
    b = x.encode('ascii')
    assert inflate(lz77(b, W, L), W, L) == b
