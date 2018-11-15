import unittest
import address_validator

test_data = ['411 Westmount Ave apt 2', '2-411 Westmount Ave', '411A Westmount Ave', 'Suite 2 411 Westmount Ave',
             '411 Apt 2 Westmount Ave', '100 Bin-scarth Avenue 2nd apt', '411 Westmount Avenue',
             '411 Westmunt Ave', 'Suite 100 234 Avenue Road, Toronto', '156 Mount Plesent Rd.',
             '256 Saint Clair Avenue West']


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

        home = address_validator.Address(test_data[5])
        self.assertTrue(home.name_body == 'Bin-Scarth', "expected Bin-Scarth, got %s" % home.name_body)
        self.assertTrue(home.unit_number == '2nd', "expected 2nd, got %s" % home.unit_number)
        self.assertTrue(home.unit_type == 'Apt', "expected Apt, got %s" % home.unit_type)
        self.assertTrue(home.street_type_suffix == 'Ave', "expected Ave, got %s" % home.street_type_suffix)
        self.assertTrue(home.address_num == '100', "expected 100, got %s" % home.address_num)

        home = address_validator.Address(test_data[6])
        self.assertTrue(home.street_type_suffix == 'Ave', "expected Ave, got %s" % home.street_type_suffix)

        home = address_validator.Address(test_data[7])
        self.assertTrue(home.name_body == 'Westmount', "expected Westmount, got %s" % home.name_body)

        home = address_validator.Address(test_data[8])
        self.assertTrue(home.name_body == 'Avenue', "expected Avenue, got %s" % home.name_body)
        self.assertTrue(home.unit_number == '100', "expected 100, got %s" % home.unit_number)
        self.assertTrue(home.unit_type == 'Ste', "expected Ste, got %s" % home.unit_type)
        self.assertTrue(home.street_type_suffix == 'Rd', "expected Rd, got %s" % home.street_type_suffix)

        home = address_validator.Address(test_data[9])
        self.assertTrue(home.name_body == 'Mount Pleasant', "expected Mount Pleasant, got %s" % home.name_body)
        self.assertTrue(home.unit_number is None, "expected None, got %s" % home.unit_number)
        self.assertTrue(home.unit_type is None, "expected None, got %s" % home.unit_type)
        self.assertTrue(home.street_type_suffix == 'Rd', "expected Rd, got %s" % home.street_type_suffix)
        self.assertTrue(home.address_num == '156', "expected 156, got %s" % home.address_num)

        home = address_validator.Address(test_data[10])
        self.assertTrue(home.dir_suffix == 'W', "expected W, got %s" % home.dir_suffix)
        self.assertTrue(home.name_body == 'St Clair', "expected St Clair, got %s" % home.name_body)
        self.assertTrue(home.unit_number is None, "expected None, got %s" % home.unit_number)
        self.assertTrue(home.unit_type is None, "expected None, got %s" % home.unit_type)
        self.assertTrue(home.street_type_suffix == 'Ave', "expected Ave, got %s" % home.street_type_suffix)
        self.assertTrue(home.address_num == '256', "expected 256, got %s" % home.address_num)



if __name__ == u'__main__':
    unittest.main()
