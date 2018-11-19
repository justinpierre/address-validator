import unittest
from address_validator import Address

test_data = ['411 Westmount Ave', '101 King']


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        """do nothing"""

    def test_address_numbers(self):
        home = Address(test_data[0])

        self.assertTrue(home.geometry == [{'x': 309218.5769999995, 'y': 4838254.662}],
                        "expected x=309218 y=4838254, got %s" % home.geometry)

        home = Address(test_data[1])
        self.assertTrue(len(home.geometry) == 3)