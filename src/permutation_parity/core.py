"""Core implementation of permutation parity via cycle decomposition."""


class PermutationError(ValueError):
    """Raised when input cannot be interpreted as a 0-indexed permutation."""


def _validate(permutation):
    """Validate that *permutation* is a 0-indexed permutation of range(n).

    We check eagerly so callers get a clear error rather than a confusing
    index or count mismatch deep in the algorithm.
    """
    if isinstance(permutation, (str, bytes)):
        raise PermutationError("permutation must be a sequence of integers, not str/bytes")
    try:
        n = len(permutation)
    except TypeError:
        raise PermutationError("permutation must be a sized iterable of integers")

    seen = set()
    for x in permutation:
        # bool is a subclass of int; we reject it so that [True, False]
        # does not silently behave like [1, 0].
        if isinstance(x, bool) or not isinstance(x, int):
            raise PermutationError("permutation elements must be integers")
        if x in seen:
            raise PermutationError("permutation contains duplicate value: {!r}".format(x))
        seen.add(x)
    if seen != set(range(n)):
        raise PermutationError(
            "permutation of length {} must be a rearrangement of range({}), "
            "but distinct values are {!r}".format(n, n, sorted(seen))
        )
    return n


def permutation_parity(permutation):
    """Return +1 if *permutation* is even, -1 if it is odd.

    A permutation is given as a sequence of integers ``p[0], p[1], ...``
    where ``p[i]`` is the image of ``i``.  Only 0-indexed permutations of
    ``range(n)`` are accepted; 1-indexed input must be shifted by the caller.

    The sign is derived from cycle decomposition: a cycle of length ``k``
    is ``(k - 1)`` transpositions, so the total parity is
    ``(-1) ** (n - cycle_count)``.  We prefer this over counting adjacent
    swaps because it visits each element once and does not depend on the
    concrete ordering of the input beyond its values.
    """
    n = _validate(permutation)
    perm = list(permutation)

    visited = [False] * n
    cycle_count = 0
    for start in range(n):
        if visited[start]:
            continue
        cycle_count += 1
        j = start
        while not visited[j]:
            visited[j] = True
            j = perm[j]
        # When the loop exits, j has returned to start; the cycle is closed.
        # We do not assert j == start here because the while-guard already
        # guarantees the cycle is well-formed under a validated permutation.

    return -1 if (n - cycle_count) % 2 else 1


def parity(permutation):
    """Return the string "even" or "odd" for *permutation*.

    Thin convenience wrapper around :func:`permutation_parity` for callers
    that prefer a human-readable label over a numeric sign.
    """
    return "even" if permutation_parity(permutation) == 1 else "odd"
