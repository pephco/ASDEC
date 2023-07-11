#!/usr/bin/python
############################################################################
# File:			callerLoadCNN.py
# Organization:	University of twente
# Group:		CAES
# Date:			31-07-2021
# Version:		1.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Calls the CNN software.
# Also provides some interfacing to explain which options are
# available.
############################################################################

# region import packages
import time
### time ###
startTime = time.time()
############
from logic import CNN
from contextlib import redirect_stdout
import getopt
import sys
from logic import logo
from logic.datatypes import Hardware
from logic.datatypes import Classification
from logic.errorHandling import ErrorHandling
# import my own files
### time ###
importTime = time.time() - startTime
startTime = time.time()
############
# endregion


############################################################################
# Function which prints the information displayed in the terminal when
# -h is provided or nothing is provided
############################################################################


def helpPrinterCNN():
    logo.logo()
    print("callerLoadCNN.py -m <model> -d <directory> -o <outDirectory")
    print("\t -m, --model: path to model including model name")
    print("\t -d, --directory: directory filled with images to classify")
    print("\t -o, --outDirectory: output directory including" +
          " file name no exstension")
    print("\t -t, --threads: Amount of threads used")
    print("\t--GPU: use GPU for inference")
    print("\t--CPU: use CPU for inference")
    print("\t--NS: binary classification of neutral and soft sweep")
    print("\t--NHS: multi-class classification of neutral, hard sweep and soft sweep")
    print("\t--NH: binary classification of neutral and hard sweep")
    print("\t -v, special option voor complete prog timing")

############################################################################
# Function which handles all different input arguments
############################################################################


def main(argv):
    ########################################################################
    # initialize some empty variables to store the values
    # even when no values are assigned easy to see that
    # no values where assigned
    ########################################################################
    mod = ''
    direc = ''
    outdirec = ''
    timeFolder = 'NULL'
    threads = '' 
    hardware = Hardware.NULL
    classification = Classification.NULL

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv, "hm:d:o:v:t:",
                                  ["model=", "directory=",
                                   "outDirectory=", "threads=",
                                   "GPU", "CPU", "NS", "NH", "NHS"])

    except getoptError:
        helpPrinterCNN()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            helpPrinterCNN()
            sys.exit()
        elif opt in ("-m", "--model"):
            mod = arg
        elif opt in ("-d", "--directory"):
            direc = arg
        elif opt in ("-o", "--outDirectory"):
            outdirec = arg
        elif opt in ("-t", "--threads"):
            threads = arg
        elif opt in ("--CPU"):
            ErrorHandling.HardwareCheck(hardware)
            hardware = Hardware.CPU
        elif opt in ("--GPU"):
            ErrorHandling.HardwareCheck(hardware)
            hardware = Hardware.GPU
        elif opt in ("--NS"):
            ErrorHandling.ClassificationCheck(classification)
            classification = Classification.NS
        elif opt in ("--NH"):
            ErrorHandling.ClassificationCheck(classification)
            classification = Classification.NH
        elif opt in ("--NHS"):
            ErrorHandling.ClassificationCheck(classification)
            classification = Classification.NHS
        elif opt == "-v":
            timeFolder = arg

    ########################################################################
    # check if all parameters are filled in
    ########################################################################
    ErrorHandling.FieldFilledInCheck([mod, direc, outdirec])
    ErrorHandling.HardwareSelected(hardware) 
    ErrorHandling.ClassificationSelected(classification)    

    ########################################################################
    # call the code which really does the work
    ########################################################################
    loadModel = CNN.Load(mod, direc, outdirec, int(threads), hardware, 
        classification)
    numberOfImages = loadModel.imageFolder()
    loadModel.generateReport()

    if not ("NULL" in timeFolder):
        ### time ###
        with open((timeFolder), 'a') as f:
            with redirect_stdout(f):
                print("Prediction import:------------:\t%.5f" %
                      importTime)
                print("Perform predictions-----------:\t%.5f" %
                      (time.time() - startTime))
                print("\tNumber of images------------:" + str(numberOfImages))      
        ############


if __name__ == "__main__":
    main(sys.argv[1:])
