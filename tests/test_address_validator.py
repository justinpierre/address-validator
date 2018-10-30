import unittest
from address_validator import address

test_data = ['411 Westmount Ave apt 2', '2-411 Westmount Ave', '411A Westmount Ave', 'Suite 2 411 Westmount Ave',
             '411 Apt 2 Westmount Ave', '100 Bin-scarth Avenue 2nd apt']



class test_Validator(unittest.TestCase):
    def setUp(self):
        self.tearDown()

    def tearDown(self):
        'do nothing'

    def test_address_numbers(self):
        home = address(test)
        home.parse_address_num()
        print(home.address_num)