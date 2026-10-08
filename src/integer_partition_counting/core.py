"""Integer partition counting via Euler's pentagonal number recurrence.

The partition function p(n) counts the number of ways to write n as a sum of
positive integers without regard to order. Euler's recurrence is:

    p(n) = sum_{k != 0} (-1)^(k-1) p(n - k(3k-1)/2)

where the generalized pentagonal numbers k(3k-1)/2 are taken for k = +-1, +-2, ...
The terms alternate in blocks of two plus, two minus, two plus, ...

We keep the sign explicit rather than precomputing a sign array so the code
mirrors the mathematical definition and stays auditable against the recurrence.

For moderate n (roughly up to a few thousand) this is a fine approach. For very
large n the memory of a full table dominates; we do not attempt asymptotically
faster methods. We return Python ints (arbitrary precision) rather than floats,
because partition counts are integers and growing them past 2^63 is expected
at the upper end of the supported range.
"""

from __future__ import annotations

from typing import List


def _sign(k: int) -> int:
    """Return (-1)^(k-1) for k >= 1.

    Equivalent to (-1)**(k-1) but written explicitly to avoid any confusion
    with how Python's ** on a negative base behaves for fractional exponents
    (which does not arise here, but stating the sign rule plainly is clearer).
    """
    return 1 if (k - 1) % 2 == 0 else -1


def _generalized_pentagonal(k: int) -> int:
    """Return the generalized pentagonal number k(3k-1)/2 for a nonzero k.

    Works for negative k as well as positive, because k(3k-1) is invariant
    under k -> 1-k in a sign-preserving sense; we just evaluate directly.
    """
    return k * (3 * k - 1) // 2


def partition_table(n: int) -> List[int]:
    """Return the list [p(0), p(1), ..., p(n)] of partition counts.

    p(0) is defined as 1 (the empty partition of 0). For n < 0 we raise
    ValueError; the recurrence and the combinatorial interpretation both
    require a nonnegative upper bound.

    We build the table forward: each entry depends only on smaller entries,
    so the loop over j from 0 to n is safe and no backward reads occur.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be nonnegative")

    table: List[int] = [0] * (n + 1)
    table[0] = 1

    for j in range(1, n + 1):
        total = 0
        k = 1
        while True:
            pent = _generalized_pentagonal(k)
            if pent > j:
                break
            total += _sign(k) * table[j - pent]
            # Negative k yields a distinct, larger pentagonal number, so we
            # must try it explicitly rather than doubling the positive term.
            neg_pent = _generalized_pentagonal(-k)
            if neg_pent > j:
                break
            total += _sign(-k) * table[j - neg_pent]
            k += 1
        table[j] = total

    return table


def partition_count(n: int) -> int:
    """Return p(n), the number of integer partitions of n.

    Convenience wrapper around partition_table. Rebuilding the whole table
    each call is wasteful if called many times; callers who need many values
    should call partition_table once and index into it.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be nonnegative")
    return partition_table(n)[n]
