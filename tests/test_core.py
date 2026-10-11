import unittest

from permutation_parity import permutation_parity, parity, PermutationError


class TestPermutationParity(unittest.TestCase):

    def test_empty_is_even(self):
        self.assertEqual(permutation_parity([]), 1)
        self.assertEqual(parity([]), "even")

    def test_single_element_is_even(self):
        self.assertEqual(permutation_parity([0]), 1)

    def test_identity_is_even(self):
        self.assertEqual(permutation_parity([0, 1, 2, 3]), 1)

    def test_single_transposition_is_odd(self):
        self.assertEqual(permutation_parity([1, 0, 2, 3]), -1)
        self.assertEqual(parity([1, 0, 2, 3]), "odd")

    def test_two_disjoint_transpositions_are_even(self):
        self.assertEqual(permutation_parity([1, 0, 3, 2]), 1)

    def test_three_cycle_is_even(self):
        # (0 1 2) -> [1, 2, 0]; a 3-cycle is 2 transpositions, hence even.
        self.assertEqual(permutation_parity([1, 2, 0]), 1)

    def test_long_odd_permutation(self):
        # (0 3)(1 2)(4 5)(6 7)(8 9) -- five disjoint transpositions.
        p = [3, 2, 1, 0, 5, 4, 7, 6, 9, 8]
        self.assertEqual(permutation_parity(p), -1)

    def test_reverse_n_is_parity_of_n_choose_2(self):
        # Reversing [0..n-1] has parity (-1)^(n(n-1)/2).  We check n=4 and n=5.
        self.assertEqual(permutation_parity([3, 2, 1, 0]), 1)
        self.assertEqual(permutation_parity([4, 3, 2, 1, 0]), 1)

    def test_tuple_input(self):
        self.assertEqual(permutation_parity((1, 0)), -1)

    def test_range_object_input(self):
        self.assertEqual(permutation_parity(range(5)), 1)

    def test_generator_rejected(self):
        # A generator has no len(), so we reject it rather than consuming it.
        with self.assertRaises(PermutationError):
            permutation_parity(x for x in range(3))

    def test_str_rejected(self):
        with self.assertRaises(PermutationError):
            permutation_parity("102")

    def test_duplicate_rejected(self):
        with self.assertRaises(PermutationError):
            permutation_parity([0, 0, 1])

    def test_missing_value_rejected(self):
        with self.assertRaises(PermutationError):
            permutation_parity([0, 1, 5])

    def test_negative_rejected(self):
        with self.assertRaises(PermutationError):
            permutation_parity([-1, 0, 1])

    def test_bool_rejected(self):
        with self.assertRaises(PermutationError):
            permutation_parity([True, False])

    def test_non_integer_rejected(self):
        with self.assertRaises(PermutationError):
            permutation_parity([0.0, 1.0])


if __name__ == "__main__":
    unittest.main()
