import pytest
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
    assert len(warnings_dict) == 4
    assert "shapes" in tapshapes_dict.keys()
    assert len(tapshapes_dict["shapes"]) == 4
    assert tapshapes_dict["shapes"][0]["shapeID"] == "#CredentialOrganization"
    assert tapshapes_dict["shapes"][1]["shapeID"] == "#Address"
    assert tapshapes_dict["shapes"][2]["shapeID"] == "#AgentTypeAlignment"
    assert tapshapes_dict["shapes"][3]["shapeID"] == "#AgentSectorTypeAlignment"
    assert len(tapshapes_dict["shapes"][0]["statement_constraints"]) == 10
    assert len(tapshapes_dict["shapes"][1]["statement_constraints"]) == 1
    assert len(tapshapes_dict["shapes"][2]["statement_constraints"]) == 3
    assert len(tapshapes_dict["shapes"][3]["statement_constraints"]) == 3
    sh3Constraints = tapshapes_dict["shapes"][3]["statement_constraints"]
    assert sh3Constraints[0]["propertyID"] == "rdf:type"
    assert sh3Constraints[2]["severity"] == "Violation"
