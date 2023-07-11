#!/usr/bin/python
############################################################################
# File:			    accuracy.py
# Organization:		University of twente
# Group:		    CAES
# Date:			    18-12-2021
# Version:		  	0.3.0
# Author:		    Matthijs Souilljee, s2211246
# Education:	  	EMSYS msc.
############################################################################
# Python program/script which is responsible for taking a summary
# file, center position, offset from the center position. Converting
# this to a total amount of populations the amount which is selective and
# the average of all center positions.
############################################################################

# region import packages
import sys
import getopt
import numpy as np
import os

from logic import str2bool
from logic.errorHandling import ErrorHandling
from logic.datatypes import Classification
from logic.logo import logo

# endregion

############################################################################
# Function which prints the information displayed in the terminal when
# -h is provided or nothing is provided
############################################################################


def HelpPrinterAccuracy():
    logo()
    print("simple program that generates an accuracy report\n")
    print("accuracy.py -i <in> -c <center> -r <range> -o <out> -p <prob> -f <fold>\n")
    print("\t -h: help option")
    print("\t -i: inputfile and/or path depending on folder mode true or false")
    print("\t -c: center position where selective region is expected")
    print("\t -r: range in which points are considered valid")
    print("\t -o: place to save the results (path + filename + exstension (e.g. sum/result.txt))")
    print("\t -f: if you want to generate the results of a whole folder (true) single file (false)")
    print("\t -p: minimal probability required to count as selective (when not desired put on 0)")



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
# Function get the TPR based on a given fpr
############################################################################
def CalculateAcc(summaryPath, centerPosition, offsetPosition,
                 minimalProbability, resultData):
    summaryData = LogFile2Array(summaryPath)
    totalAmount = 0
    withinRangeAmount = 0
    averageCenterPostion = 0
    for data in summaryData:
        if ((data[2] <= centerPosition + offsetPosition) and
                (data[2] >= centerPosition - offsetPosition) and
                (data[4] > minimalProbability)):
            withinRangeAmount += 1
        totalAmount += 1
        averageCenterPostion += abs(data[2] - centerPosition)
    averageCenterPostion = averageCenterPostion / totalAmount
    return np.append(resultData,
                     np.array([[summaryPath,
                                averageCenterPostion,
                                withinRangeAmount,
                                totalAmount,
                                (withinRangeAmount/totalAmount),
                                averageCenterPostion
                                ]]),
                     axis=0)


############################################################################
# program processes the inputs
############################################################################
def main(argv):
    ########################################################################
    # initialize some variables
    ########################################################################
    summaryPath = ''
    outputPath = ''
    centerPosition = -1.0
    offsetPosition = -1.0
    minimalProbability = -1.0
    folderMode = False

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv, "hi:c:o:r:p:f:",
                                  ["in=", "center=",
                                   "range=", "out=",
                                   "prob=", "fold="])
    except getoptError:
        HelpPrinterAccuracy()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            HelpPrinterAccuracy()
            sys.exit(2)
        elif opt in ("-i", "--in"):
            summaryPath = arg
        elif opt in ("-c", "--center"):
            centerPosition = float(arg)
        elif opt in ("-r", "--range"):
            offsetPosition = float(arg)
        elif opt in ("-o", "--out"):
            outputPath = arg
        elif opt in ("-p", "--prob"):
            minimalProbability = float(arg)
        elif opt in ("-f", "--fold"):
            folderMode = str2bool.str2bool(arg)

    ########################################################################
    # check if all arguments are filled in
    ########################################################################
    if (len(summaryPath) == 0 or centerPosition == -1.0
            or offsetPosition == -1.0 or len(outputPath) == 0
            or minimalProbability == -1.0):
        print("ERROR: Not all fields are filled in correctly")
        HelpPrinterAccuracy()
        sys.exit(2)

    # create an empty numpy array where the results are saved
    resultData = np.empty((0, 6), float)

    print("Calculating accuracy")

    ########################################################################
    # get the summary data from the file
    # and perform the necesarry calculations
    ########################################################################
    if folderMode:
        count = 0
        with os.scandir(summaryPath) as folder:
            for textFile in folder:
                if textFile.is_file():
                    print("processing file number: " + str(count))
                    resultData = CalculateAcc(summaryPath + textFile.name,
                                              centerPosition,
                                              offsetPosition,
                                              minimalProbability,
                                              resultData)
                    count += 1
    else:
        resultData = CalculateAcc(summaryPath, centerPosition,
                                  offsetPosition, minimalProbability,
                                  resultData)

    print("Saving results")

    ########################################################################
    # save everything to a file
    ########################################################################
    np.savetxt(outputPath, resultData[:, :], fmt="%s")

    print("Done")


if __name__ == "__main__":
    main(sys.argv[1:])
