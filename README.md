# permutation_parity

Determines the sign (even or odd parity) of a permutation from its cycle decomposition.

```python
from permutation_parity import permutation_parity, parity

permutation_parity([1, 0, 2, 3])   # -1  (odd: one transposition)
parity([1, 0, 2, 3])              # "odd"
permutation_parity([1, 2, 0])      #  1  (even: 3-cycle = 2 transpositions)
```

The library exists because computing the sign of a permutation is a small,
self-contained operation that is easy to get subtly wrong by hand.  The cycle
method is used: a cycle of length *k* equals *k - 1* transpositions, so the
overall sign is `(-1) ** (n - cycle_count)`.  This visits each element once and
avoids the bookkeeping of decomposing into adjacent swaps.

Input is a 0-indexed permutation given in one-line notation: element `i` maps
to `p[i]`.  One-indexed input is not supported; shift it yourself.  Only full
permutations of `range(n)` are accepted — partial arrays, duplicates, or
non-integer entries raise `PermutationError`.
