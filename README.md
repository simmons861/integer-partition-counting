# integer_partition_counting

Computes the number of integer partitions p(n) using Euler's pentagonal number recurrence. Pure Python, standard library only.

## Usage

```python
from integer_partition_counting import partition_count, partition_table

print(partition_count(10))   # 42
print(partition_table(5))    # [1, 1, 2, 3, 5, 7]
```

`partition_count(n)` returns p(n) as a Python int. `partition_table(n)` returns the list `[p(0), p(1), ..., p(n)]`. Both raise `ValueError` for negative `n` and `TypeError` for non-int input (including `bool`, which is a subclass of `int` and is rejected deliberately).

## Why this exists

Partition counts appear in combinatorics and number theory. The recurrence

```
p(n) = sum_{k != 0} (-1)^(k-1) p(n - k(3k-1)/2)
```

lets you build the table for all values up to n in O(n^1.5) time and O(n) memory, which is enough for moderate n (roughly up to a few thousand). We build the whole table because the recurrence reads earlier entries, and we return Python ints rather than floats because partition counts are exact integers that exceed 2^63 well before the table becomes unwieldy.

For very large n the memory of holding the full table dominates and asymptotically faster methods would be needed; this library does not attempt those.

## Edge cases

- `p(0) = 1` by convention (the empty partition). The table for `n = 0` is `[1]`.
- `partition_count` rebuilds the entire table each call. If you need several values, call `partition_table` once and index into the result.
- The generalized pentagonal numbers for positive and negative k are distinct except for k = 0, which we skip; the recurrence requires both signs.

## Layout

- `src/integer_partition_counting/__init__.py` exports `partition_count` and `partition_table`.
- `src/integer_partition_counting/core.py` contains the recurrence.
- `tests/test_core.py` runs under `python -m unittest discover -s tests` with `PYTHONPATH=src`.
