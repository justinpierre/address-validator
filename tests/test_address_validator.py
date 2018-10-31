import unittest
from address_validator import Address

test_data = ['411 Westmount Ave apt 2', '2-411 Westmount Ave', '411A Westmount Ave', 'Suite 2 411 Westmount Ave',
             '411 Apt 2 Westmount Ave', '100 Bin-scarth Avenue 2nd apt']


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        """do nothing"""

    def test_address_numbers(self):
        home = Address(test_data[0])
        self.assertTrue(home.address_num == '411', "expected address number to be 411, found %s" % home.address_num)
        self.assertTrue(home.unit_number == '2', "expected unit number to be 2, found %s" % home.unit_number)

        home = Address(test_data[2])
        self.assertTrue(home.address_num == '411', "expected address number to be 411, found %s" % home.address_num)
        self.assertTrue(home.unit_number == 'A', "expected unit number to be A, found %s" % home.unit_number)


if __name__ == u'__main__':
    unittest.main()
