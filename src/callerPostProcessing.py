#!/usr/bin/python
############################################################################
# File:			callerPostProcessing.py
# Organization:	University of twente
# Group:		CAES
# Date:			31-07-2021
# Version:		1.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Calls the Post processing software.
# Also provides some interfacing to explain which options are
# available.
############################################################################

# region import packages
import time
### time ###
startTime = time.time()
############
import sys
import getopt
from contextlib import redirect_stdout

# import my own files
from logic import PostProcessing
from logic import logo
### time ###
importTime = time.time() - startTime
startTime = time.time()
############
# endregion

############################################################################
# Function which prints the information displayed in the terminal when
# -h is provided or nothing is provided
############################################################################


def helpPrinterPost():
    logo.logo()
    print("callerPostProcessing.py -m <mode>" +
          " -i <inputdirectory> -o <outputdirectory>" +
          " -s <outputdirectorysummary>" +
          " -x <outputdirectorypost>" +
          " -a <parama> -b <paramb>")
    print("\t-h: help option")
    print("\t-i: directory containing log files to process")
    print("\t-x: output directory + name pre-post log files (empty is not saving)")
    print("\t-o: output directory + name post log files (empty is not saving)")
    print("\t-s: output directory + name summary files (empty is not saving)")
    print("\tMode 1: Window based on entries in the file")
    print("\t\t -a: stepsize in entries in the file")
    print("\t\t -b: windowsize in entries in the file")
    print("\tMode 2: Window based on position")
    print("\t\t -a: stepsize in position")
    print("\t\t -b: windowsize in position")
    print("\tMode 3: Grid normal mode")
    print("\t\t -a: gridsize in interger value (if set to zero just " +
          "\n\t\t take the amount of entries in the file)")
    print("\t\t -b: max distance range in position")
    print("\tMode 4: Grid no max size check (always enforces grid size)")
    print("\t\t -a: gridsize in interger value")
    print("\t\t -b: max distance range")
    print("\t -v, special option voor complete prog timing")
    

############################################################################
# Function which handles all different input arguments
############################################################################


def main(argv):
    ### time ###
    startTime = time.time()
    ############
    ########################################################################
    # initialize some empty variables to store the values
    # even when no values are assigned easy to see that
    # no values where assigned
    ########################################################################
    mod = ''
    indirec = ''
    outdirec = 'NULL'
    outSummary = 'NULL'
    outprepost = 'NULL'
    param1 = ''
    param2 = ''
    timeFolder = 'NULL'

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv, "hm:i:o:a:b:s:v:x:",
                                  ["mode=", "inputdirectory=",
                                   "outputdirectory=",
                                   "outputdirectorysummary=",
                                   "outputdirectorypost=",
                                   "parama=", "paramb"])
    except getoptError:
        helpPrinterPost()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            helpPrinterPost()
            sys.exit()
        elif opt in ("-m", "--mode"):
            mod = arg
        elif opt in ("-i", "--inputdirectory"):
            indirec = arg
        elif opt in ("-o", "--outputdirectory"):
            outdirec = arg
        elif opt in ("-a", "--parama"):
            param1 = arg
        elif opt in ("-b", "--paramb"):
            param2 = arg
        elif opt in ("-s", "--outputdirectorysummary"):
            outSummary = arg
        elif opt == "-v":
            timeFolder = arg
        elif opt in ("-x","--outputdirectorypost"):
            outprepost = arg

    ########################################################################
    # check if all parameters are filled in
    ########################################################################
    if (len(mod) == 0 or len(indirec) == 0 or
            len(param1) == 0 or len(param2) == 0):
        print("ERROR: not all fields are filled in!")
        helpPrinterPost()
        sys.exit()

    if (float(param1) <= 0 or float(param2) <= 0):
        print("ERROR: some values are zero or smaller then zero")
        sys.exit()

    ########################################################################
    # Determine mode and call the child class corresponding
    ########################################################################
    if (int(float(mod)) == 1):
        call = PostProcessing.WindowData(indirec, outdirec,
                                         outSummary, outprepost,
                                         int(float(param1)),
                                         int(float(param2)))
    elif (int(float(mod)) == 2):
        call = PostProcessing.WindowPos(indirec, outdirec,
                                        outSummary, outprepost,
                                        float(param1),
                                        float(param2))
    elif (int(float(mod)) == 3):
        call = PostProcessing.GridSize(indirec, outdirec,
                                       outSummary, outprepost,
                                       int(float(param1)),
                                       float(param2),
                                       True)
    elif (int(float(mod)) == 4):
        call = PostProcessing.GridSize(indirec, outdirec,
                                       outSummary,
                                       int(float(param1)),
                                       int(float(param2)),
                                       False)
    else:
        print("ERROR: unknown mode")
        sys.exit(2)

    call.PostFolder()

    if(timeFolder != "NULL"):
        ### time ###
        with open((timeFolder), 'a') as f:
            with redirect_stdout(f):
                print("Post import-------------------:\t%.5f" %
                    importTime)
                print("Post processing---------------:\t%.5f" %
                      (time.time() - startTime))
        ############

if __name__ == "__main__":
    main(sys.argv[1:])
