#!/usr/bin/python
############################################################################
# File:			callerBitmap.py
# Organization:	University of twente
# Group:		CAES
# Date:			31-07-2021
# Version:		1.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Calls the bitmapConverter software.
# Also provides some interfacing to explain which options are
# available.
############################################################################

# region import packages
import time

from logic.errorHandling import ErrorHandling
### time ###
startTime = time.time()
############
import sys
import getopt
from contextlib import redirect_stdout
import shlex
import subprocess

# import my own files
from logic import errorHandling
from logic import bitmapConverter
from logic import str2bool
from logic import logo
from logic import vcfConversion
### time ###
importTime = time.time() - startTime
startTime = time.time()
############
# endregion


############################################################################
# function for printing the helper information
############################################################################


def helpPrinter():
    logo.logo()
    print("callerBitmap.py -i <input file> -o <output file> -w <window enable> -s" +
          " <step size of the window> -l <length of the window> -c <center enable>" +
          " -z <range center region> -m <multiplication Position> -a <start population>" +
          " -e <end population> -x <memorySize>")
    print("\t -h: help option")
    print("\t -i, --ifile: give the path to the input file generated by either MS" +
          " or MSSEL \n\tmust include the file with exstension")
    print("\t -o, --ofile: output directory where the image will be placed \n\tmust" +
          " include the file name without exstension (.png)")
    print("\t -w, --windowEnb: option to use window mode give either true or false")
    print("\t -s, --windowStep: Only required if windowed mode is enabled \n\t" +
          "Otherwise option not needed\n\t" +
          "Gives the amount the window jumps forward each itteration \n\tif this is 1" +
          " all windows of the image will be made")
    print("\t -l, --windowSize: Only required if windowed mode is enabled \n\tOtherwise" +
          " option not needed\n\tArgument gives the size of the window")
    print("\t -c, --extractionEnb: Use for mssel to extract the selective sweep\n\tfrom the" +
          " extraction of the dataset")
    print("\t -p, --extractionPoint: Only required if extraction mode is enabled \n\tOtherwise" +
          " option not needed\n\tArgument gives the extraction point (given in position value)")
    print("\t -z, --extractionOff: Only required if extraction mode is enabled \n\tOtherwise" +
          " option not needed\n\tArgument gives the range from the extraction point")
    print("\t -m, --multiplicationPosition: Multiplication for all positions")
    print("\t -a, --startPopulation: population to start from generation\n" +
          "\tif not set take whole file")
    print("\t -e, --endPopulation: population to which to generate\n" +
          "\tif not set take whole file")
    print("\t -x, --memorySize: parsing vcf file, memory consumption (input * 2)")
    print("\t -X, --chromosomeLength: parsing vcf file, total chromosome length (def: 10)")
    print("\t -v: special option voor complete prog timing (def 100000)")

############################################################################
# Function which handles all different input arguments
############################################################################


def main(argv):
    ########################################################################
    # initialize some empty variables to store the values
    # even when no values are assigned easy to see that
    # no values where assigned
    ########################################################################
    inputfile = ''
    outputfile = ''
    windowTrigger = ''
    stepSize = ''
    size = ''
    extractionTrigger = ''
    extractionSize = ''
    startPos = '0.0'
    endPos = '0.0'
    mulPos = '1.0'
    timeFolder = 'NULL'
    extractionPoint = ''
    memorySize = '10'
    chromosomeLength = '100000'

    ############################################################################
    # get all the arguments from the commandline
    ############################################################################
    try:
        opts, args = getopt.getopt(argv, "hi:o:w:s:l:c:z:p:m:a:e:v:x:X:",
                                   ["ifile=", "ofile=", "windowEnb=",
                                    "windowStep=", "windowSize=", "extractionEnb=",
                                    "extractionOff=", "extractionPoint="
                                    "multiplicationPosition=", "startPopulation=", 
                                    "endPopulation=", "memorySize=", "chromosomeLength="])
    except getoptError:
        helpPrinter()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            helpPrinter()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-w", "--windowEnb"):
            windowTrigger = arg
        elif opt in ("-s", "--windowStep"):
            stepSize = arg
        elif opt in ("-l", "--windowSize"):
            size = arg
        elif opt in ("-c", "--extractionEnb"):
            extractionTrigger = arg
        elif opt in ("-z", "--extractionOff"):
            extractionSize = arg
        elif opt in ("-m", "--multiplicationPosition"):
            mulPos = arg
        elif opt in ("-a", "--startPopulation"):
            startPos = arg
        elif opt in ("-e", "--endPopulation"):
            endPos = arg
        elif opt in ("-p", "--extractionPoint"):
            extractionPoint = arg
        elif opt in ("-x", "--memorySize"):
            memorySize = arg
        elif opt in ("-X", "--chromosomeLength"):
            chromosomeLength = arg
        elif opt == "-v":
            timeFolder = arg

    ############################################################################
    # perform a check if the two mandatory boolean arguments are provided
    ############################################################################
    if len(windowTrigger) == 0 or len(extractionTrigger) == 0:
        helpPrinter()
        print("ERROR: boolean for enabling window mode and/or enabling "
              "the center not set or not set correctly!")
        sys.exit()

    ############################################################################
    # determine based on the triggers which other arguments are required
    # and set the other ones to one, because they are not used in the
    # bitmap converter program
    ############################################################################
    if (str2bool.str2bool(windowTrigger) == True
        and str2bool.str2bool(extractionTrigger) == True):
        errorHandling.ErrorHandling.FieldFilledInCheck(
            [inputfile, outputfile, stepSize, size, extractionSize, extractionPoint]
        )
    elif (str2bool.str2bool(windowTrigger) == True
        and str2bool.str2bool(extractionTrigger) == False):
        errorHandling.ErrorHandling.FieldFilledInCheck(
            [inputfile, outputfile, stepSize, size]
        )
        extractionSize="1"
        extractionPoint = "1"
    elif (str2bool.str2bool(windowTrigger) == False
        and str2bool.str2bool(extractionTrigger) == True):
        errorHandling.ErrorHandling.FieldFilledInCheck(
            [inputfile, outputfile, extractionSize, extractionPoint]
        )
        stepSize="1"
        size="1"
    else:
        errorHandling.ErrorHandling.FieldFilledInCheck(
            [inputfile, outputfile]
        )
        stepSize="1"
        size="1"
        extractionSize="1"

    ############################################################################
    # check if the values are larger then zero otherwise infinite loop possible
    # in the bitmap converter
    ############################################################################
    errorHandling.ErrorHandling.GreaterThenZeroCheck(
        [stepSize, size, extractionSize, startPos, endPos]
    )
        
    ############################################################################
    # If the file is in the vcf format call the RAiSD parser
    ############################################################################
    if vcfConversion.vcfConversion(inputfile, chromosomeLength, memorySize):
        inputfile = inputfile + ".ms"
    
    ############################################################################
    # call the code which really does the work
    ############################################################################
    bitmapConverter.ImageConversion(inputfile, outputfile,
                                    str2bool.str2bool(windowTrigger),
                                    int(float(stepSize)),
                                    int(float(size)),
                                    str2bool.str2bool(extractionTrigger),
                                    int(float(extractionSize)),
                                    float(extractionPoint),
                                    float(mulPos),
                                    int(float(startPos)),
                                    int(float(endPos)))
    
    if not ("NULL" in timeFolder):
        ### time ###
        with open((timeFolder), 'a') as f:
            with redirect_stdout(f):
                print("File running:-----------------:\t" + str(inputfile))
                print("Bitmap import-----------------:\t%.5f" %
                    importTime)
                print("Bitmap conversion-------------:\t%.5f" %
                    (time.time() - startTime))
        ############


if __name__ == "__main__":
    main(sys.argv[1:])
