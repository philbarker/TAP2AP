import pytest
from dctap import csvreader  # , TAPShape, TAPStatementConstraint
from dctap.config import get_config
from AP import AP, PropertyStatement
from tap2ap import TAP2APConverter

tapFileName = "tests/TestData/tap.csv"
configFileName = "tests/TestData/dctap.yml"
namespaceFileName = "tests/TestData/namespaces.csv"
aboutFileName = "tests/TestData/about.csv"
shapesFileName = "tests/TestData/shapes.csv"


@pytest.fixture(scope="module")
def test_Converter():
    Converter = TAP2APConverter(tapFileName, configFileName)
    return Converter


def test_initConverter(test_Converter):
    c = test_Converter
    assert c
    assert len(c.tap["warnings_dict"]) == 4
    assert "shapes" in c.tap["shapes_dict"].keys()
    shapes_list = c.tap["shapes_dict"]["shapes"]
    assert len(shapes_list) == 4
    assert shapes_list[0]["shapeID"] == "#CredentialOrganization"
    assert shapes_list[1]["shapeID"] == "#Address"
    assert shapes_list[2]["shapeID"] == "#AgentTypeAlignment"
    assert shapes_list[3]["shapeID"] == "#AgentSectorTypeAlignment"
    s4 = shapes_list[3]
    assert len(s4["statement_constraints"]) == 3
    s4sc2 = s4["statement_constraints"][2]
    assert s4sc2["propertyID"] == "ceterms:targetNode"


def test_convert_namespaces(test_Converter):
    c = test_Converter
    assert c.ap.namespaces == {}
    c.convert_namespaces("TAP")
    assert len(c.ap.namespaces) == 16
    assert c.ap.namespaces["_"] == "http://example.org/"
    assert c.ap.namespaces["xsd"] == "http://www.w3.org/2001/XMLSchema#"
    c.convert_namespaces("csv", namespaceFileName)
    assert len(c.ap.namespaces) == 18
    assert c.ap.namespaces["sh"] == "http://www.w3.org/ns/shacl#"


def test_load_AP_metadata(test_Converter):
    c = test_Converter
    assert c.ap.metadata == {}
    c.load_AP_Metadata(aboutFileName)
    assert c.ap.metadata["url"] == "tap.csv"
    assert c.ap.metadata["date"] == "2021-03-26"


def test_load_shapeInfo(test_Converter):
    c = test_Converter
    assert c.ap.shapeInfo == {}
    c.ap.load_shapeInfo(shapesFileName)
    assert (
        c.ap.shapeInfo["#CredentialOrganization"]["label"]
        == "Credential Organization Shape"
    )
    assert c.ap.shapeInfo["#Address"]["target"] == "ceterms:address"
    assert c.ap.shapeInfo["#Address"]["targetType"] == "ObjectsOf"


def test_check_shapeID(test_Converter):
    c = test_Converter
    sh_id = "#CredentialOrganization"
    sh_id = c.check_shapeID(sh_id)
    assert sh_id == "#CredentialOrganization"
    sh_id = 2
    with pytest.raises(TypeError) as e:
        sh_id = c.check_shapeID(sh_id)
    assert str(e.value) == "shapeID must be a string."
    sh_id = "notAShapeID"
    with pytest.raises(ValueError) as e:
        sh_id = c.check_shapeID(sh_id)
    assert str(e.value) == "No shape info for notAShapeID"


def test_convert_propertyIDs(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    p_id = "test1, test2 test3,test4;test5\ntest6"
    c.convert_propertyIDs(p_id, ps)
    for p in ["test1", "test2", "test3", "test4", "test5", "test6"]:
        assert p in ps.properties
    p_id = ["test1"]
    with pytest.raises(TypeError) as e:
        c.convert_propertyIDs(p_id, ps)
    assert str(e.value) == "Properties must be passed in a string."


def test_convert_labels(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    label = "test one"
    c.convert_labels(label, ps)
    ps.labels == [{"en": "test one"}]
    label = ["test one"]
    with pytest.raises(TypeError) as e:
        c.convert_labels(label, ps)
    assert str(e.value) == "Labels must be passed in a string."


def test_convert_mandatory(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    m = "False"
    c.convert_mandatory(m, ps)
    assert ps.mandatory == False
    m = "True"
    c.convert_mandatory(m, ps)
    assert ps.mandatory == True
    m = "No"
    c.convert_mandatory(m, ps)
    assert ps.mandatory == False
    m = True
    with pytest.raises(TypeError) as e:
        c.convert_mandatory(m, ps)
    assert str(e.value) == "Value for mandatory must be a string."
    m = "Allowed"
    with pytest.raises(ValueError) as e:
        c.convert_mandatory(m, ps)
    assert str(e.value) == "Value for mandatory not recognised: Allowed"


def test_convert_repeatable(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    r = "False"
    c.convert_repeatable(r, ps)
    assert ps.repeatable == False
    r = "True"
    c.convert_repeatable(r, ps)
    assert ps.repeatable == True
    r = "No"
    c.convert_repeatable(r, ps)
    assert ps.repeatable == False
    r = True
    with pytest.raises(TypeError) as e:
        c.convert_repeatable(r, ps)
    assert str(e.value) == "Value for repeatable must be a string."
    r = "Allowed"
    with pytest.raises(ValueError) as e:
        c.convert_repeatable(r, ps)
    assert str(e.value) == "Value for repeatable not recognised: Allowed"


def test_convert_valueNodeTypes(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    vNT = "IRI, bnode"
    c.convert_valueNodeTypes(vNT, ps)
    assert "IRI" in ps.valueNodeTypes
    assert "bnode" in ps.valueNodeTypes
    vNT = ["IRI", "bnode"]
    with pytest.raises(TypeError) as e:
        c.convert_valueNodeTypes(vNT, ps)
    assert str(e.value) == "Value for node types must be a string."


def test_convert_valueDataTypes(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    vDT = "xsd:date; xsd:time"
    c.convert_valueDataTypes(vDT, ps)
    assert "xsd:date" in ps.valueDataTypes
    assert "xsd:time" in ps.valueDataTypes
    vDT = ["xsd:date", "xsd:time"]
    with pytest.raises(TypeError) as e:
        c.convert_valueDataTypes(vDT, ps)
    assert str(e.value) == "Value for data types must be a string."


def test_convert_valueConstraints(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    vC = """orgType:AssessmentBody
orgType:Business"""
    c.convert_valueConstraints(vC, ps)
    assert "orgType:AssessmentBody" in ps.valueConstraints
    assert "orgType:Business" in ps.valueConstraints
    vC = 2
    with pytest.raises(TypeError) as e:
        c.convert_valueConstraints(vC, ps)
    assert str(e.value) == "Value for constraints must be a string."


def test_convert_valueConstraintType(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    vCT = "pattern"
    c.convert_valueConstraintType(vCT, ps)
    assert ps.valueConstraintType == "pattern"
    vCT = None
    with pytest.raises(TypeError) as e:
        c.convert_valueConstraintType(vCT, ps)
    assert str(e.value) == "Value for constraint type must be a string."


def test_convert_shapes(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    shapes = "#Address,#Contact"
    c.ap.add_shapeInfo("#Address", {"label": "Address"})
    c.ap.add_shapeInfo("#Contact", {"label": "Contact"})
    c.convert_valueShapes(shapes, ps)
    for sh in ["#Address", "#Contact"]:
        assert sh in ps.valueShapes
    shapes = ["#Address", "#Contact"]
    with pytest.raises(TypeError) as e:
        c.convert_valueShapes(shapes, ps)
    assert str(e.value) == "Value for shapes must be a string."
    shapes = "#notAShapeID"
    with pytest.raises(ValueError) as e:
        c.convert_valueShapes(shapes, ps)
    assert str(e.value) == "No shape info for #notAShapeID"


def test_convert_notes(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    note = "test one"
    c.convert_notes(note, ps)
    assert ps.notes == {"en": "test one"}
    note = 42
    with pytest.raises(TypeError) as e:
        c.convert_notes(note, ps)
    assert str(e.value) == "Notes must be passed in a string."


def test_convert_severity(test_Converter):
    c = test_Converter
    ps = PropertyStatement()
    sev = "Violation"
    c.convert_severity(sev, ps)
    assert ps.severity == "Violation"
    sev = None
    with pytest.raises(TypeError) as e:
        c.convert_severity(sev, ps)
    assert str(e.value) == "Value for severity must be a string."


def test_convert_TAP_AP(test_Converter):
    c = test_Converter
    c.convert_TAP_AP()
