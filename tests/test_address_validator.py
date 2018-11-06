import unittest
import address_validator

test_data = ['411 Westmount Ave apt 2', '2-411 Westmount Ave', '411A Westmount Ave', 'Suite 2 411 Westmount Ave',
             '411 Apt 2 Westmount Ave', '100 Bin-scarth Avenue 2nd apt', '411 Westmount Avenue',
             '411 Westmunt Ave', 'Suite 100 Avenue Road, Toronto']


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        """do nothing"""

    def test_address_numbers(self):
        home = address_validator.Address(test_data[0])
        self.assertTrue(home.address_num == '411', "expected address number to be 411, found %s" % home.address_num)
        self.assertTrue(home.unit_number == '2', "expected unit number to be 2, found %s" % home.unit_number)
        self.assertTrue(home.street_type_suffix == 'Ave', "expected Ave, got %s" % home.street_type_suffix)

        home = address_validator.Address(test_data[2])
        self.assertTrue(home.address_num == '411', "expected address number to be 411, found %s" % home.address_num)
        self.assertTrue(home.unit_number == 'A', "expected unit number to be A, found %s" % home.unit_number)

        home = address_validator.Address(test_data[6])
        self.assertTrue(home.street_type_suffix == 'Ave', "expected Ave, got %s" % home.street_type_suffix)

        home = address_validator.Address(test_data[7])
        self.assertTrue(home.name_body == 'Westmount', "expected Westmount, got %s" % home.name_body)

        home = address_validator.Address(test_data[8])
        self.assertTrue(home.name_body == 'Avenue', "expected Avenue, got %s" % home.name_body)

if __name__ == u'__main__':
    unittest.main()
