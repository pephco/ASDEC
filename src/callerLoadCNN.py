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
    CPU = False
    GPU = False

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv, "hm:d:o:v:t:",
                                  ["model=", "directory=",
                                   "outDirectory=", "threads=",
                                   "GPU", "CPU"])

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
            CPU = True
        elif opt in ("--GPU"):
            GPU = True
        elif opt == "-v":
            timeFolder = arg

    ########################################################################
    # check if all parameters are filled in
    ########################################################################
    if (len(mod) == 0 or len(direc) == 0 or len(outdirec) == 0):
        helpPrinterCNN()
        print("ERROR: not all fields are filled in!")
        sys.exit(1)
        
    if (not((CPU and GPU == False) or 
        (CPU == False and GPU))):
        print("ERROR: Selected none or multiple hardware settings")
        print("only use one --GPU or --CPU")
        sys.exit(1)

    ########################################################################
    # call the code which really does the work
    ########################################################################
    loadModel = CNN.Load(mod, direc, outdirec, int(threads), CPU, GPU)
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
