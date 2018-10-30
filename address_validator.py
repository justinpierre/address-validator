catch_unit_types = ['apt', 'suite', 'ste', 'unit']

class address:
    def __init__(self, original_address):
        self.original_address = original_address
        self.unit_number = None
        self.address_num = None

    @property
    def original_address(self):
        return self._original_address

    @original_address.setter
    def original_address(self,original_address):
        self._original_address = original_address

    @property
    def address_num(self):
        return self._address_num

    @address_num.setter
    def address_num(self,address_num):
        self._address_num = address_num

    @property
    def name_body(self):
        return self

    @property
    def dir_prefix(self):
        return self

    @property
    def dir_suffix(self):
        return self

    @property
    def street_type_suffix(self):
        return self

    @property
    def unit_number(self):
        return self._unit_number

    @unit_number.setter
    def unit_number(self, unit_number):
        self._unit_number = unit_number


    @property
    def unit_type(self):
        return self

    def parse_address_num(self):
        # TODO pop matched unit numbers from numbers_at_position
        # also split at '-' unless it's preceded by 'Bin', 'De' or 'Mid'
        address_parts = []
        for p in self.original_address.split(' '):
            if '-' in p and True not in [x in p for x in ['Bin', 'De', 'Mid']]:
                for x in p.split('-'):
                    address_parts.append(x)
            else:
                address_parts.append(p)

        numbers_at_position = []
        print(address_parts)
        for part in address_parts:
            # find any numbers
            if part.isdigit():
                numbers_at_position.append(address_parts.index(part))
            # find cases of mixed number and unit like 100A
            for position in part:
                if position.isdigit() and address_parts.index(part) not in numbers_at_position:
                    numbers_at_position.append(address_parts.index(part))

        for position in numbers_at_position:
            # if a unit type is adjacent to a number, call that number the unit number
            if (address_parts[position - 1].lower() in catch_unit_types and position > 0) \
                    or (address_parts[position + 1].lower() in catch_unit_types and position < len(address_parts) -1):
                self.unit_number = address_parts[position]

        # if you only have one number, its the address number
        if len(numbers_at_position) == 1:
            self.address_num = address_parts[numbers_at_position[0]]

        print(self.address_num)
        # if you have two adjacent numbers, the first one is unit
        if len(numbers_at_position) == 2 and numbers_at_position[1] - numbers_at_position[0] == 1:
            self.address_num = address_parts[numbers_at_position[1]]
            self.unit_number = address_parts[numbers_at_position[0]]

        # TODO catch mixed numbers with letters


        return self


def main():
    test_data = ['411 Westmount Ave apt 2', '2-411 Westmount Ave', '411A Westmount Ave', 'Suite 2 411 Westmount Ave',
                 '411 Apt 2 Westmount Ave', '100 Bin-scarth Avenue 2nd apt']
    for test in test_data:
        hocd pyme = address(test)
        home.parse_address_num()


if __name__ == '__main__':
    main()
