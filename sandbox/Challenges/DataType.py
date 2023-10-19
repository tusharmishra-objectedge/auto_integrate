import requests
from app.api_formatter.base import APIFormatter
from app.file_handler.json_handler import JSONHandler

import json
import os

from sandbox.Llama2Sandbox.llama2API import prompt_llama2API

# Data SF Registered Business Locations
urlDataSF = "https://data.sfgov.org/resource/g8m3-pdis.json"

jsonTypes = ["String", "Number", "Boolean", "Null", "Object", "Array"]
pythonTypes = ["str", "int", "float", "bool", "None", "dict", "list"]

acceptableConversions = {
    "str": {"int", "float", "bool", "list"},
    "int": {"str", "float", "bool"},
    "float": {"str", "int", "bool"},
    "bool": {"str", "int", "float"},
    "None": {"None"},
    "dict": {"str"},
    "list": {"str"}
}

transformations = {}

def checkConversion(fromType, toType):
    '''
    Checks if a conversion is possible between two types
    Args:
        fromType:
        toType:

    Returns: True if conversion is possible, False otherwise
    '''
    if fromType in acceptableConversions:

        return fromType == toType or toType in acceptableConversions[fromType]
    else:
        return False

def convertType(field1, type1, type2):
    '''
    Converts a field from one type to another. Updates the transformations dictionary
    Args:
        field1: field from api1
        type1: type of field1
        type2: type of mapped field in api1

    Returns: converted field

    '''
    if type1 == type2:
        return field1

    # From string
    if type1 == 'str':
        if type2 == 'int':
            transformations[field1] = 'int'
            return int(field1)
        elif type2 == 'float':
            transformations[field1] = 'float'
            return float(field1)
        elif type2 == 'bool':
            transformations[field1] = 'bool'
            return bool(field1)
        elif type2 == 'list':
            transformations[field1] = 'list'
            return [field1]
    # From int
    elif type1 == 'int':
        if type2 == 'str':
            transformations[field1] = 'str'
            return str(field1)
        elif type2 == 'float':
            transformations[field1] = 'float'
            return float(field1)
        elif type2 == 'bool':
            transformations[field1] = 'bool'
            return bool(field1)
    # From float
    elif type1 == 'float':
        if type2 == 'str':
            transformations[field1] = 'str'
            return str(field1)
        elif type2 == 'int':
            transformations[field1] = 'int'
            return int(field1)
        elif type2 == 'bool':
            transformations[field1] = 'bool'
            return bool(field1)
    # From bool
    elif type1 == 'bool':
        if type2 == 'str':
            transformations[field1] = 'str'
            return str(field1)
        elif type2 == 'int':
            transformations[field1] = 'int'
            return int(field1)
        elif type2 == 'float':
            transformations[field1] = 'float'
            return float(field1)
    # From list
    elif type1 == 'list':
        if type2 == 'str':
            transformations[field1] = 'str'
            return str(field1)
    # From None
    elif type1 == 'None':
        transformations[field1] = 'None'
        return None
    # From dict
    elif type1 == 'dict':
        if type2 == 'str':
            transformations[field1] = 'str'
            return str(field1)

    return None


if __name__ == "__main__":

    input_file = os.path.join("../../demo", "inputs/mockAPI1.json")
    file1 = JSONHandler(input_file)
    inputs = file1.read()

    api_formatter = APIFormatter(inputs)
    api1, api2 = api_formatter.format()

    with open('Inputs/dt1.json') as json_file:
        data = json.load(json_file)

    # print(api1)
    # print(api2)

    # Add fields to a set for each api
    api1Mapped = set(x for x in api1.keys())
    api2Mapped = set(x for x in api2.keys())

    api1Unmapped = set()
    api2Unmapped = set()

    # From the output, remove the mapped fields from the set, to check against mapped and unmaped
    for a1, a2 in data['mappedFields'].items():
        api1Mapped.remove(a1)
        api2Mapped.remove(a2)

    # Add the unmapped fields to the set
    for field in data['unmappedFields']:
        api1Unmapped.add(field)

    # Add the unmapped fields to the set
    for field in api2Mapped:
        api2Unmapped.add(field)

    print(f'api1unmapped: {api1Unmapped}')
    print(f'api2unmapped: {api2Unmapped}')

    userMapped = {
        "tt1": "typeTest1",
        "tt2": "typeTest2",
        "tt3": "typeTest3",
        "id": "id",
        "created": "createdAt"
    }

    for key, val in userMapped.items():
        keyTyep = api1[key]
        valType = api2[val]

        if checkConversion(keyTyep, valType):
            print(f'{key}: {api1[key]} can be converted to {val}: {api2[val]}')
            convert = convertType(key, api1[key], api2[val])
            print(f'Converted value: {convert}')
            print(f'After conversion types: {convert.__class__.__name__} and {api2[val]}')
        else:
            print(f'{key}: {api1[key]} cannot be converted to {val}: {api2[val]}')

        print()

    print(transformations)