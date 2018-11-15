import unittest
import address_validator
import geocoder

test_data = ['411 Westmount Ave']


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        """do nothing"""

    def test_address_numbers(self):
        home = address_validator.Address(test_data[0])
        geometry = geocoder.geocode(home)
        self.assertTrue(geometry == {'x': 309218.5769999995, 'y': 4838254.662},
                        "expected x=309218 y=4838254, got %s" % geometry)

