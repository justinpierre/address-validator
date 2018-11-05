import requests
import re
import os
import json
import arcpy


def scrape_rest_endpoint(urls, folder):
    """The source code of the tool."""
    arcpy.AddMessage(u"Fetching GeoJSON files from Map Service")
    layersToSync = {}

    # mapServiceUrl should be a list of urls pointing at map service or feature service layers.
    # each should end in "MapServer/<some number>" or "FeatureServer/<some number>"

    # load contents of feature service info page
    for mapServiceUrl in urls:
        mapServiceContents = requests.get("{}?f=json".format(mapServiceUrl))
        mapServiceData = mapServiceContents.json()

        # deal with layer names that start with a number
        layerName = safeName(mapServiceData['name'])
        if not re.match(u'[a-zA-Z_]', layerName):
            layerName = u"_{}".format(layerName)

        # add the layer name as a key to the layersToSync dictionary with an empty list as the value
        layersToSync[layerName] = []
        count = 0

        # fetch esriFieldTypeOID name
        try:
            for field in mapServiceData['fields']:
                if field['type'] == 'esriFieldTypeOID':
                    layerOID = field['name']
        except:
            continue

        # cycle through queries to scrape all data
        while True:
            downloadDataUrl = "{}/query?where={}%3E%3D{}&outFields=*&f=json&returnGeometry=True&orderByFields={}". \
                format(mapServiceUrl, layerOID, str(count), layerOID)
            arcpy.AddMessage(downloadDataUrl)
            layerData = requests.get(downloadDataUrl)
            features = layerData.json()
            featurecount = len(features['features'])

            # if no features returned, you're done and move on to the next layer
            if featurecount == 0:
                break

            # otherwise, find the last objecit id you retrieved and pass that to your query next time
            nextoid = features['features'][featurecount - 1]['attributes'][layerOID] + 1

            # save the output json to the mirror directory
            if not os.path.exists(os.path.join("{}/{}".format(folder, mapServiceData['id']))):
                os.makedirs(os.path.join("{}/{}".format(folder, mapServiceData['id'])))
            layerGeojsonfile = os.path.join("{}/{}/{}{}.json".format(
                folder, mapServiceData['id'], layerName, str(count)))

            layerGeojson = open(layerGeojsonfile, 'w+')
            json.dump(features, layerGeojson)

            # populate the value in layersToSync with the list of JSON fiels associated with the layer
            layersToSync[layerName].append("{}{}".format(
                safeName(layerName), str(count)))
            layerGeojson.close()
            count = nextoid
    print(layersToSync)

    print('locating JSON data')
    downloadedJson = {}
    layers = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(folder)):
        layers = []
        for layer in filenames:
            if layer[-5:] == ".json":
                layers.append(layer)
        if layers != [] or None:
            downloadedJson[dirpath] = layers

    arcpy.AddMessage('Moving geojson files to merged file gdb')

    mergedGDBName = u'merged_layers.gdb'
    mergedGDB = os.path.join(folder, mergedGDBName)
    if not os.path.exists(mergedGDB):
        arcpy.CreateFileGDB_management(folder, mergedGDBName)

    for key in downloadedJson:

        # cycle through the files in each download directory
        for layer in downloadedJson[key]:

            # copy the json file into the mergedlayers.gdb
            if arcpy.Exists(os.path.join(mergedGDB, layer.split('.')[0])) == False:
                arcpy.JSONToFeatures_conversion(os.path.join(key, layer), os.path.join(mergedGDB, layer))

            # skip cases where the datatype will cause things to fail
            layertype = arcpy.Describe(os.path.join(mergedGDB, layer.split('.')[0]))
            if layertype.datasetType not in ["FeatureClass", "FeatureLayer"]:
                arcpy.AddMessage(
                    "Not syncing layer: {} because of datatype {}".format(layer, layertype.datasetType))
                arcpy.Delete_management(os.path.join(mergedGDB, layer.split('.')[0]))
                continue

            # use the layersToSync dictionary to identify what layer the json file is supposed to be merged to
            for mergedLayer in layersToSync:
                if layer.split('.')[0] in layersToSync[mergedLayer]:
                    if arcpy.Exists(os.path.join(mergedGDB, mergedLayer)):
                        arcpy.Append_management(os.path.join(mergedGDB, layer.split('.')[0]), os.path.join
                        (mergedGDB, mergedLayer))
                    else:
                        arcpy.FeatureClassToFeatureClass_conversion \
                            (os.path.join(mergedGDB, layer.split('.')[0]), mergedGDB, mergedLayer)
                    arcpy.Delete_management(os.path.join(mergedGDB, layer.split('.')[0]))

    return


def safeName(name, lowerCase=True, keepSpaces=False, substituteInto=None):
    """
    # Converts a string to a safe name for use as directories or table names.  The output replaces all non-alphanumeric
    # characters with underscores (optionally, keeping space characters)

    :param name:
    :param lowerCase:
    :param keepSpaces:
    :param substituteInto:
    :return:
    """
    safe = name

    if lowerCase:
        safe = name.lower()

    if keepSpaces:  # keep spaces if requested (default == True)
        safe = re.sub(u'([^\\s\\w]|_)', u'_', safe, flags=re.UNICODE)
    else:
        safe = re.sub(u'([^\\w]|_)', u'_', safe, flags=re.UNICODE)

    if substituteInto is not None and u'%s' in substituteInto:
        safe = substituteInto % safe

    return safe

scrape_rest_endpoint(['https://gis.toronto.ca/arcgis/rest/services/primary/cot_geospatial_mtm/MapServer/2'],
                     r'C:\GFX data work\City of Toronto, ON')