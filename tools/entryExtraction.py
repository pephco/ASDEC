import os
import sys
import numpy as np
import re
from contextlib import redirect_stdout
import getopt

############################################################################
# Function which prints the information displayed in the terminal when
# -h is provided or nothing is provided
############################################################################


def helpPrinter():
    print("entryExtraction.py -i <input directory> -o <output file> -p <percentage>")

############################################################################
# Function convert the txt file to a numpy array which could be plotted
############################################################################


def LogFile2Array(textFileName):
    logfileData = np.empty((0, 5), float)
    try:
        with open(textFileName, 'r') as logfile:
            for line in logfile.readlines():
                point = line.split(' ')
                firstPosition = float(point[0])
                lastPosition = float(point[1])
                middlePosition = float(point[2])
                probNeutral = float(point[3])
                probSelective = float(point[4])
                logfileData = np.append(logfileData,
                                        np.array(
                                            [[firstPosition,
                                              lastPosition,
                                              middlePosition,
                                              probNeutral,
                                              probSelective,
                                              ]]),
                                        axis=0)
    except IOError:
        print("ERROR: File could not be loaded")
        return
    return logfileData

############################################################################
# program processes the inputs
############################################################################

    
def main(argv):
    inputDirectory = ''
    outputDirectory = ''
    percentage = ''
    try:
        opts, ars = getopt.getopt(argv, "hi:o:p:",
                                  [])

    except getoptError:
        helpPrinter()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            helpPrinter()
            sys.exit()
        elif opt in ("-i"):
            inputDirectory = arg
        elif opt in ("-o"):
            outputDirectory = arg
        elif opt in ("-p"):
            percentage = arg

    if (len(inputDirectory) == 0 or len(outputDirectory) == 0 or len(percentage) == 0):
        print("ERROR: not all fields are filled in!")
        helpPrinter()
        sys.exit()
        
    if (float(percentage) < 0 or float(percentage) > 1):
        print("ERROR: percentage not between range 0 and 1")
        helpPrinter()
        sys.exit()
            
    data = LogFile2Array(inputDirectory)
    data = data[data[:, 4].argsort()]
    data = np.flip(data, 0)
    index = round((len(data) - 1) * float(percentage))
    resultData = data[0:index,:]
    np.savetxt(outputDirectory, resultData[:][:], fmt="%s")
    
if __name__ == "__main__":
    main(sys.argv[1:])