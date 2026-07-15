import unittest

from .temperature import celsius_to_fahrenheit, describe_temperature


class TemperatureTests(unittest.TestCase):
    def test_conversion(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212)

    def test_description_boundaries(self):
        self.assertEqual(describe_temperature(-1), "below freezing")
        self.assertEqual(describe_temperature(0), "freezing point")
        self.assertEqual(describe_temperature(19.9), "cool")
        self.assertEqual(describe_temperature(20), "warm")


if __name__ == "__main__":
    unittest.main()
