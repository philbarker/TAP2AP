#!/usr/bin/env python

from dctap import csvreader  # , TAPShape, TAPStatementConstraint
from dctap.config import get_config
from AP import AP, PropertyStatement
from tap2ap import TAP2APConverter
from getch import getch, pause

tapFileName = "tests/TestData/tap.csv"
configFileName = "tests/TestData/dctap.yml"
namespaceFileName = "tests/TestData/namespaces.csv"
aboutFileName = "tests/TestData/about.csv"
shapesFileName = "tests/TestData/shapes.csv"

if __name__ == "__main__":
    print("\nTAP2AP comprises some methods for converting a Dublin Core Tabular Application Profile (TAP) to a python Application Profile data object (AP).\n\nOther programs can do interesting things with the AP.\n\nThere is no command line interface. \n\n")
    pause('Press any key to continue...')
    print("\nLet's use test data create an example application profile and then display it.")
    print("* TAP file is: ", tapFileName)
    print("* TAP config file is: ", configFileName)
    print("* AP namespace file is: ", namespaceFileName)
    print("* AP metadata file is: ", aboutFileName)
    print("* AP shapes info file is: ", shapesFileName)
    pause('\nPress any key to continue...')
    c = TAP2APConverter(tapFileName, configFileName) # Initializa a converter
                                                     # This also reads the TAP
    c.convert_namespaces("TAP") # Convert any namespaces in the TAP
    c.convert_namespaces("csv", namespaceFileName) # Convert AP namespcs
    c.ap.load_metadata(aboutFileName) # load metadata about the AP
    c.ap.load_shapeInfo(shapesFileName) # load info about shapes in AP
    c.convert_TAP_AP() # convert data from TAP into AP
    c.ap.dump() # print out the AP
