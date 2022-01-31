import pytest
from pprint import PrettyPrinter
from dctap import csvreader  # , TAPShape, TAPStatementConstraint
from dctap.config import get_config
from AP import AP, PropertyStatement

tapFileName = "tests/TestData/tap.csv"
configFileName = "tests/TestData/dctap.yml"
namespaceFileName = "tests/TestData/namespaces.csv"
aboutFileName = "tests/TestData/about.csv"
shapesFileName = "tests/TestData/shapes.csv"


def test_loadTAP():
    config_dict = get_config(configFileName)
    with open(tapFileName, "r") as csv_fileObj:
        csvreader_output = csvreader(csv_fileObj, config_dict)
    tapshapes_dict, warnings_dict = csvreader_output
    assert len(warnings_dict) == 2
    assert "shapes" in tapshapes_dict.keys()
    assert len(tapshapes_dict["shapes"]) == 2
    assert tapshapes_dict["shapes"][0]["shapeID"] == "BookShape"
    assert tapshapes_dict["shapes"][1]["shapeID"] == "AuthorShape"
    assert len(tapshapes_dict["shapes"][0]["statement_constraints"]) == 4
    assert len(tapshapes_dict["shapes"][1]["statement_constraints"]) == 3
    sh0Constraints =  tapshapes_dict["shapes"][0]["statement_constraints"]
    sh1Constraints = tapshapes_dict["shapes"][1]["statement_constraints"]
    assert sh0Constraints[0]["propertyID"] == "dct:title"
    assert sh0Constraints[1]["propertyID"] == "dct:creator"
    assert sh0Constraints[2]["propertyID"] == "sdo:isbn"
    assert sh0Constraints[3]["propertyID"] == "rdf:type"
    assert sh1Constraints[0]["propertyID"] == "rdf:type"
    assert sh1Constraints[1]["propertyID"] == "foaf:givenName"
    assert sh1Constraints[2]["propertyID"] == "foaf:familyName"
    assert sh0Constraints[2]["propertyLabel"] == "ISBN-13"
    assert sh0Constraints[2]["mandatory"] == "false"
    assert sh0Constraints[2]["repeatable"] == "false"
    assert sh0Constraints[2]["valueNodeType"] == "literal"
    assert sh0Constraints[2]["valueDataType"] == "xsd:string"
    assert sh0Constraints[2]["valueConstraint"] == "^(\\\\d{13})?$"
    assert sh0Constraints[2]["valueConstraintType"] == "pattern"
