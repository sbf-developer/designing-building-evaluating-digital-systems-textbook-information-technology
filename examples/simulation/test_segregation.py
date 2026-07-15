import unittest

from .segregation import is_happy, make_grid, run


class SegregationTests(unittest.TestCase):
    def test_empty_neighbourhood_is_happy(self):
        grid = [[None, None], [None, "A"]]
        self.assertTrue(is_happy(grid, 1, 1, 0.5))

    def test_seed_reproduces_initial_grid(self):
        self.assertEqual(make_grid(seed=3), make_grid(seed=3))
        self.assertNotEqual(make_grid(seed=3), make_grid(seed=4))

    def test_run_is_bounded(self):
        result = run(make_grid(size=4, seed=2), max_steps=3)
        self.assertLessEqual(result.steps, 3)


if __name__ == "__main__":
    unittest.main()
