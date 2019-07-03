"""Generic tools used in project."""

from itertools import tee


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    # pylint: disable=C
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


__all__ = ['pairwise']
