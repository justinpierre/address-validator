import re
from stringdist import levenshtein
from data.street_name_body import names
import requests

unit_types = {'Apt': ['apt', 'apartment'], 'Ste': ['suite'], 'Unit': ['unit']}
street_dir = {'W': ['West', 'W.'], 'E': ['East', 'E.'], 'S': ['South', 'S.'], 'N': ['North', 'N.']}
catch_unit_types = ['apt', 'suite', 'ste', 'unit', 'apartment']
muns = ['toronto', 'etobicoke', 'scarborough', 'york', 'east york']
street_types = {'St': ['Street', 'St.'],
                'Ave': ['Avenue', 'Ave.'],
                'Rd': ['Road', 'Rd.'],
                'Blvd': ['Boulevard', 'Blvd.'],
                'Lane': ['Ln'],
                'Way': ['Wy'],
                'Ter': ['Terrace'],
                'Pk': ['Park'],
                'Wds': ['Woods'],
                'Pl': ['Place'],
                'Gdns': ['Gardens'],
                'Grv': ['Grove'],
                'Wood': ['Wd'],
                'Lwn': ['Lawn'],
                'Cres': ['Crescent'],
                'Crcl': ['Circle'],
                'Trl': ['Trail'],
                'Cs': ['Close'],
                'View': ['Vw'],
                'Grn': ['Green'],
                'Mews': ['Mws'],
                'Pkwy': ['Parkway'],
                'Walk': ['Wlk'],
                'Crct': ['Circuit'],
                'Line': ['Line'],
                'Hill': ['Hill.'],
                'Ptwy': ['Pathway'],
                'Crt': ['Court'],
                'Gt': ['Gate'],
                'Path': ['Path'],
                'Hts': ['Heights'],
                'Sq': ['Square']
                }


class Address:
    def __init__(self, original_address):
        self.original_address = original_address

        address_parts = []
        for p in self.original_address.split(' '):
            if '-' in p and True not in [x in p for x in ['Bin', 'De', 'Mid']]:
                for x in p.split('-'):
                    address_parts.append(x.strip())
            else:
                address_parts.append(p.strip().replace(',', ''))
        address_parts = list(filter(None, address_parts))
        if address_parts[len(address_parts)-1].lower() in muns:
            self.municipality = address_parts[len(address_parts)-1]
            address_parts.pop(len(address_parts)-1)
        else:
            self.municipality = None

        self.address_num, self.unit_number, pop_numbers = self.parse_address_num(address_parts)
        for pn in pop_numbers:
            address_parts.pop(pn)

        self.dir_suffix, pop_numbers = self.parse_dir_suffix(address_parts)
        if pop_numbers:
            address_parts.pop(pop_numbers)

        self.street_type_suffix, pop_numbers = self.parse_street_type(address_parts)

        if pop_numbers:
            address_parts.pop(pop_numbers)

        self.unit_type, pop_numbers = self.parse_unit_type(address_parts)

        if pop_numbers:
            address_parts.pop(pop_numbers)

        self.name_body = self.parse_name_body(address_parts)

        self.geometry = self.geocode()

    @property
    def original_address(self):
        return self._original_address

    @original_address.setter
    def original_address(self, original_address):
        self._original_address = original_address

    @property
    def address_num(self):
        return self._address_num

    @address_num.setter
    def address_num(self, address_num):
        self._address_num = address_num

    @property
    def name_body(self):
        return self._name_body

    @name_body.setter
    def name_body(self, name_body):
        self._name_body = name_body

    @property
    def dir_prefix(self):
        return self

    @property
    def dir_suffix(self):
        return self._dir_suffix

    @dir_suffix.setter
    def dir_suffix(self, dir_suffix):
        self._dir_suffix = dir_suffix

    @property
    def street_type_suffix(self):
        return self._street_type_suffix

    @street_type_suffix.setter
    def street_type_suffix(self, street_type_suffix):
        self._street_type_suffix = street_type_suffix

    @property
    def unit_number(self):
        return self._unit_number

    @unit_number.setter
    def unit_number(self, unit_number):
        self._unit_number = unit_number

    @property
    def unit_type(self):
        return self._unit_type

    @unit_type.setter
    def unit_type(self, unit_type):
        self._unit_type = unit_type

    @property
    def municipality(self):
        return self._municipality

    @municipality.setter
    def municipality(self, municipality):
        self._municipality = municipality

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry

    def parse_address_num(self, address_parts):
        numbers_at_position = []
        topop = []
        unit_number, address_num = None, None
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
                    or (address_parts[position + 1].lower() in catch_unit_types and position < len(address_parts) - 1):
                unit_number = address_parts[position]
                topop.append(position)
                numbers_at_position.pop(numbers_at_position.index(position))

        # if you have two adjacent numbers, the first one is unit
        if len(numbers_at_position) == 2 and numbers_at_position[1] - numbers_at_position[0] == 1:
            address_num = address_parts[numbers_at_position[1]]
            unit_number = address_parts[numbers_at_position[0]]
            topop.extend([numbers_at_position[0], numbers_at_position[1]])
            numbers_at_position.pop(0)
            topop.sort(reverse=True)
            return address_num, unit_number, topop

        # if you only have one number, its the address number
        if len(numbers_at_position) == 1:
            # Units that are letters mixed in with the address number like 100A
            letter_number = list(filter(None, re.split('(\d+)', address_parts[numbers_at_position[0]])))
            if len(letter_number) > 1:
                address_num = letter_number[0]
                unit_number = letter_number[1]
            else:
                address_num = address_parts[numbers_at_position[0]]
            topop.append(numbers_at_position[0])
        topop.sort(reverse=True)
        return address_num, unit_number, topop

    def parse_street_type(self, address_parts):
        resp = None, None
        for ap in address_parts:
            for k, l in street_types.items():
                if ap.lower() == k.lower():
                    resp = k, address_parts.index(ap)
                for v in l:
                    if ap.lower() == v.lower():
                        resp = k, address_parts.index(ap)

        return resp

    def parse_unit_type(self, address_parts):
        for ap in address_parts:
            for k, l in unit_types.items():
                if ap.lower() == k.lower():
                    return k, address_parts.index(ap)
                for v in l:
                    if ap.lower() == v.lower():
                        return k, address_parts.index(ap)
        return None, None


    def parse_dir_suffix(self, address_parts):
        for ap in address_parts:
            for k, l in street_dir.items():
                if ap.lower() == k.lower():
                    return k, address_parts.index(ap)
                for v in l:
                    if ap.lower() == v.lower():
                        return k, address_parts.index(ap)
        return None, None

    def parse_name_body(self, address_parts):
        # stick together the remaining parts
        # TODO return best matches under a value
        s = ' '
        name = s.join(address_parts)
        match = [None, 10]
        if name in names:
            return name

        for n in names:
            score = levenshtein(name, n)
            if score < match[1]:
                match = [n, score]

        return match[0]

    def geocode(self):
        query_url = 'http://gis.toronto.ca/arcgis/rest/services/primary/cot_geospatial_mtm/MapServer/2/query'
        where = ''
        fields = {'ADDRESS_NUMBER': self.address_num,
                  'LINEAR_NAME': self.name_body,
                  'LINEAR_NAME_TYPE': self.street_type_suffix,
                  'LINEAR_NAME_DIR': self.dir_suffix,
                  'MUNICIPALITY_NAME': self.municipality}
        for f, m in fields.items():
            if m:
                if where != '':
                    where += ' AND '
                where += "%s = '%s'" % (f, m)

        params = {"where": where,
                  "outFields": "*",
                  "returnGeometry": "true",
                  "returnIdsOnly": "false",
                  "returnCountOnly": "false",
                  "f": "pjson"
                  }
        resp = requests.get(query_url, params)
        geoms = []
        for f in resp.json()['features']:
            geoms.append(f['geometry'])
        return geoms