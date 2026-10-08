import unittest

from integer_partition_counting import partition_count, partition_table


class TestPartitionCount(unittest.TestCase):
    def test_zero_is_one(self):
        self.assertEqual(partition_count(0), 1)

    def test_one_is_one(self):
        self.assertEqual(partition_count(1), 1)

    def test_two_is_two(self):
        self.assertEqual(partition_count(2), 2)

    def test_known_values(self):
        # OEIS A000041
        expected = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
        for n, p in enumerate(expected):
            self.assertEqual(partition_count(n), p, f"p({n}) should be {p}")

    def test_larger_known_value(self):
        self.assertEqual(partition_count(20), 627)
        self.assertEqual(partition_count(30), 5604)
        self.assertEqual(partition_count(50), 204226)


class TestPartitionTable(unittest.TestCase):
    def test_zero_length(self):
        self.assertEqual(partition_table(0), [1])

    def test_length_is_n_plus_one(self):
        self.assertEqual(len(partition_table(10)), 11)
        self.assertEqual(len(partition_table(1)), 2)

    def table_matches_individual_counts(self):
        t = partition_table(15)
        for n in range(16):
            self.assertEqual(t[n], partition_count(n))

    def test_first_eleven_match(self):
        self.assertEqual(
            partition_table(10), [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
        )


class TestValidation(unittest.TestCase):
    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            partition_count(-1)
        with self.assertRaises(ValueError):
            partition_table(-5)

    def test_bool_rejected(self):
        # bool is a subclass of int; we reject it explicitly to avoid
        # surprising silent behaviour from True/False being treated as 1/0.
        with self.assertRaises(TypeError):
            partition_count(True)
        with self.assertRaises(TypeError):
            partition_table(False)

    def test_non_int_rejected(self):
        with self.assertRaises(TypeError):
            partition_count(3.0)
        with self.assertRaises(TypeError):
            partition_table("5")


if __name__ == "__main__":
    unittest.main()
