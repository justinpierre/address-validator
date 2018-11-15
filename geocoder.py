import requests

query_url = 'http://gis.toronto.ca/arcgis/rest/services/primary/cot_geospatial_mtm/MapServer/2/query'
def geocode(address):
    print(address.address_num)
    params = {"where": "ADDRESS_NUMBER = '%s' AND LINEAR_NAME = '%s'" % (address.address_num, address.name_body),
              "outFields": "*",
              "returnGeometry": "true",
              "returnIdsOnly": "false",
              "returnCountOnly": "false",
              "f": "pjson"
              }
    resp = requests.get(query_url, params)
    return resp.json()['features'][0]['geometry']