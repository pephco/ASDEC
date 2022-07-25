#!/usr/bin/python
############################################################################
# File:			    TPRFPR.py
# Organization:		University of twente
# Group:		    CAES
# Date:			    18-12-2021
# Version:		  	0.2.0
# Author:		    Matthijs Souilljee, s2211246
# Education:	  	EMSYS msc.
############################################################################
# Python program/script which is responsible for taking both the summary
# of the neutral and selected data. first of all both the summaries are
# sorted and afterwards a fixed fpr percentage is chosen and based on
# the given FPR the TPR could be calculated.
############################################################################

# region import packages
import sys
import getopt
import numpy as np
import os

from logic.datatypes import Classification
from logic.errorHandling import ErrorHandling
from logic import logo
from logic import str2bool
# endregion

############################################################################
# Function which prints the information displayed in the terminal when
# -h is provided or nothing is provided
############################################################################


def HelpPrinterTPRFPR():
    logo.logo()
    print("simple program that generates a true positive rate (TPR)" +
          "based on a given false positive rate (FPR)\n")
    print("TPRFPR.py -n <neutral> -s <selected> -f <FPR> -o <out> -r <run>" +
          " -d <folder>\n")
    print("\t -h: help option")
    print("\t -n: folder and/or file that includes neutral summary data")
    print("\t -s: folder and/or file that includes selective summary data")
    print("\t -f: FPR (between 0 and 1)")
    print("\t -o: output path + filename.txt")
    print("\t -r: do a complete run of all FPR from 0 to 1 with steps of 0.05")
    print("\t -d: all files in a folder please use predifend nameing format" +
          " form LoadCNN.py for this")
    print("\t--NS: binary classification of neutral and soft sweep")
    print("\t--NHS: multi-class classification of neutral, hard sweep and soft sweep")
    print("\t--NH: binary classification of neutral and hard sweep")

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

def CalculateTPRBinary(neutralData, selectiveData, FPR):
    # make a sorted lost of the neutral data and selective data
    # sorted is from small to large value according to the probability
    # of selective.
    neutralData = neutralData[neutralData[:, 4].argsort()]
    selectiveData = selectiveData[selectiveData[:, 4].argsort()]

    # flip the data so that the large prob of being selective is on
    # position 0
    neutralData = np.flip(neutralData, 0)
    selectiveData = np.flip(selectiveData, 0)

    # find the index based on the fpr
    fprIndex = round((len(neutralData) - 1) * float(FPR))

    # find the value corresponding to the fpr based on the index
    fprProbSelec = neutralData[fprIndex, 4]

    # TPR set to zero, because if not changed all points are below
    index = 0
    TPR = 1.0
    for dataLine in selectiveData:
        # print(dataLine[4])
        if dataLine[4] <= fprProbSelec:
            TPR = index / (len(selectiveData))
            break
        index += 1
    return fprProbSelec, TPR


############################################################################
# folder mode func
############################################################################


def Folder(summarySelective, summaryNeutral, FPR):
    # create an empty numpy array where the results are saved
    tempData = np.empty((0, 4), float)
    with os.scandir(summarySelective) as folderSelective:
        for textFileSelective in folderSelective:
            if textFileSelective.is_file():
                if "_sel_" in textFileSelective.name:
                    traj = textFileSelective.name[7:9]
                    if (not traj.isnumeric()):
                        traj = textFileSelective.name[7:8]
                    # print(textFileSelective.name)
                    with os.scandir(summaryNeutral) as folderNeutral:
                        for textFileNeutral in folderNeutral:
                            if textFileNeutral.is_file():
                                if (str(traj) + "_neu_") in textFileNeutral.name:
                                    compPathNeu = summaryNeutral + textFileNeutral.name
                                    compPathSel = summarySelective + textFileSelective.name
                                    neutralData = LogFile2Array(
                                        compPathNeu)
                                    selectiveData = LogFile2Array(
                                        compPathSel)
                                    fprProbSelec, TPR = CalculateTPRBinary(
                                        neutralData, selectiveData, FPR)
                                    tempData = np.append(tempData,
                                                         np.array([[compPathSel,
                                                                    fprProbSelec,
                                                                    FPR,
                                                                    TPR]]),
                                                         axis=0)
    return tempData

############################################################################
# single file mode func
############################################################################


def Single(summarySelective, summaryNeutral, FPR):
    # print("single file")
    neutralData = LogFile2Array(summaryNeutral)
    selectiveData = LogFile2Array(summarySelective)
    ########################################################################
    # now calculate the TPR
    ########################################################################
    fprProbSelec, TPR = CalculateTPRBinary(neutralData, selectiveData, FPR)
    ########################################################################
    # append to the results
    ########################################################################
    return np.array([[summarySelective,
                      fprProbSelec,
                      FPR,
                      TPR]])


############################################################################
# folder mode or single file
############################################################################


def FolderOrSingle(summarySelective, summaryNeutral, FPR,
                   folderMode):
    if folderMode:
        return Folder(summarySelective, summaryNeutral, FPR)
    else:
        return Single(summarySelective, summaryNeutral, FPR)


############################################################################
# program processes the inputs
############################################################################


def main(argv):
    ########################################################################
    # initialize some variables
    ########################################################################
    summaryNeutral = ''
    summarySelective = ''
    FPR = ''
    outputPath = ''
    fullRun = False
    folderMode = False
    classification = Classification.NULL

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv, "hn:s:f:d:o:r:",
                                        ["neutral=", "selective=",
                                         "fpr=", "folder=",
                                         "out=", 'run=',
                                         "NS", "NH", "NHS"])
    except getoptError:
        HelpPrinterTPRFPR()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            HelpPrinterTPRFPR()
            sys.exit(2)
        elif opt in ("-n", "--neutral"):
            summaryNeutral = arg
        elif opt in ("-s", "--selective"):
            summarySelective = arg
        elif opt in ("-f", "--fpr"):
            FPR = arg
        elif opt in ("-o", "--out"):
            outputPath = arg
        elif opt in ("-d", "--folder"):
            folderMode = str2bool.str2bool(arg)
        elif opt in ("-r", "--run"):
            fullRun = str2bool.str2bool(arg)
        elif opt in ("--NS"):
            ErrorHandling.ClassificationCheck(classification)
            classification = Classification.NS
        elif opt in ("--NH"):
            ErrorHandling.ClassificationCheck(classification)
            classification = Classification.NH
        elif opt in ("--NHS"):
            ErrorHandling.ClassificationCheck(classification)
            classification = Classification.NHS

    ########################################################################
    # check if all arguments are filled in
    ########################################################################
    ErrorHandling.FieldFilledInCheck([summaryNeutral, summarySelective,
                                      FPR, outputPath])
    ErrorHandling.ClassificationSelected(classification)
    print("Calculating TPR based on a FPR of " + str(FPR))

    if (classification == Classification.NHS):
        print("Not supported")
        return

    #########################################################################
    # get the summary data from the file
    # and perform the necesarry calculations
    ########################################################################
    # if full run is enabled go through all fpr values
    if fullRun:
        resultData = np.empty((0, 4), float)
        i = 0.0
        while(i <= 1.0001):
            print("full run FPR " + str(i))
            # create an empty numpy array where the results are saved
            resultData = np.append(resultData, FolderOrSingle(summarySelective,
                                                              summaryNeutral,
                                                              i,
                                                              folderMode),
                                   axis=0)
            i += 0.05
    else:
        resultData = FolderOrSingle(summarySelective, summaryNeutral, FPR,
                                    folderMode)

    print("Saving results")

    ########################################################################
    # save everything to a file
    ########################################################################
    np.savetxt(outputPath, resultData[:, :], fmt="%s")


if __name__ == "__main__":
    main(sys.argv[1:])
