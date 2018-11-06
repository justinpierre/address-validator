import requests
import json
import os

resp = requests.get('http://gis.toronto.ca/arcgis/rest/services/primary/cot_geospatial_mtm/MapServer/2/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=LINEAR_NAME_TYPE&outStatistics=%5B%7B%22statisticType%22%3A+%22count%22%2C%22onStatisticField%22%3A+%22LINEAR_NAME_TYPE%22%2C+%22outStatisticFieldName%22%3A+%22TYPE%22%7D%5D%0D%0A&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=pjson')
with open(os.path.join(os.getcwd, 'data', 'street_type_suffix.py'), 'w+') as outfile:
    json.dump(resp.json(), outfile)

street_body_name = []
abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for letter in abc:
    resp = requests.get('http://gis.toronto.ca/arcgis/rest/services/primary/cot_geospatial_mtm/MapServer/2/query?where=1%3D1+and+linear_name+like+%27{}%25%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=LINEAR_NAME&groupByFieldsForStatistics=LINEAR_NAME&outStatistics=%5B%7B%22statisticType%22%3A+%22count%22%2C%22onStatisticField%22%3A+%22LINEAR_NAME%22%2C+%22outStatisticFieldName%22%3A+%22TYPE%22%7D%5D%0D%0A&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=pjson'.format(letter))

    for f in resp.json()['features']:
        street_body_name.append(f['attributes']['LINEAR_NAME'])

with open(os.path.join(os.getcwd(), 'data', 'street_name_body.py'), 'w+') as outfile:
    json.dump(street_body_name, outfile)


