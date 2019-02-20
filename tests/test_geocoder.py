import unittest
from address_validator import Address

test_data = ['411 Westmount Ave', '101 King', '167 old orchard, york']


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

        home = Address(test_data[2])
        self.assertTrue(home.name_body == 'Old Orchard', 'expected Old Orchard, got %s' % home.name_body)
        self.assertTrue(home.address_num == '167', 'expected 167, got %s' % home.address_num)
        self.assertTrue(home.municipality == 'york', 'expected york, got %s' % home.municipality)
        print(home.geometry)