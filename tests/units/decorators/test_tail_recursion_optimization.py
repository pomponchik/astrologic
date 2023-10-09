import sys

from astrologic import no_recursion


def test_big_recursion():
    @no_recursion
    def c(b):
        if b == sys.getrecursionlimit() * 10:
            return b
        return c(b + 1)

    assert c(0) == sys.getrecursionlimit() * 10
