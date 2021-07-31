############################################################################
# File:			    PostProcessing.py
# Organization:		University of twente
# Group:		    CAES
# Date:			    21-04-2021
# Version:		    0.5.0
# Author:		    Matthijs Souilljee, s2211246
# Education:	  	EMSYS msc.
############################################################################
# Post processing for log files, includes three different functionalities.
# - Grid size approach: give a max amount of points corresponding to
# a grid, from this grid a certain max and min of base pair positions
# are taken and averaged.
# - Window size approach: give a window size and step size,
# based on amount of data.
# - Window size approach position: give a window size and step size
# based on base pair positions.
# All approaches are implemented within the corresponding child class
############################################################################


# region import packages
from abc import ABCMeta, abstractmethod
import math
import pathlib
import numpy as np
import os
# endregion

############################################################################
# Parent class
############################################################################


class PostProcessing:
    __metaclass__ = ABCMeta
    ########################################################################
    # class constructor
    ########################################################################
    # region

    def __init__(self, logfilePath, outLogFilePath, outSummary, outPrePostLog):
        self.logfilePath = logfilePath
        self.outLogFilePath = outLogFilePath
        self.outSummary = outSummary
        self.outPrePostLog = outPrePostLog
    # endregion

    ########################################################################
    # public methods
    ########################################################################
    # region
    def PostFolder(self):
        count = 1
        self.summary = np.empty((0, 6), float)
        with os.scandir(self.logfilePath) as folder:
            for textFile in folder:
                if textFile.is_file():
                    print("processing file number: " + str(count))
                    self.PerformPost(textFile.name)
                    count += 1
        # save the self.summary numpy array to a seperate file
        if (self.outSummary != "NULL"):
            self.SaveSummary()

    @abstractmethod
    def PerformPost(self, textFileName):
        raise NotImplementedError("ERROR: Must override by childeren")

    @abstractmethod
    def SaveSummary(self):
        raise NotImplementedError("ERROR: Must override by childeren")

    def CreateSummaryLine(self):
        print("create summary line")
        idx = np.where(np.around(self.logfileDataPost[:, 4], 5) ==
                       np.amax(np.around(self.logfileDataPost[:, 4], 5)))
        if (len(idx[0]) == 1):
            idx = idx[0][0]
        else:
            avgIdx = int((len(idx[0])-1)/2)
            idx = idx[0][avgIdx]
        print(idx)
        self.summary = np.append(self.summary,
                                 np.array([self.logfileDataPost[idx, :]]),
                                 axis=0)

    def Textfile2Array(self, textFileName):
        self.logfileData = np.empty((0, 5), float)
        try:
            with open(self.logfilePath + textFileName, 'r') as logfile:
                for line in logfile.readlines():
                    point = line.split(' ')
                    firstPosition = float(point[0])
                    lastPosition = float(point[1])
                    middlePosition = float(point[2])
                    probNeutral = float(point[3])
                    probSelective = float(point[4])
                    self.logfileData = np.append(self.logfileData,
                                                 np.array(
                                                     [[firstPosition,
                                                       lastPosition,
                                                       middlePosition,
                                                       probNeutral,
                                                       probSelective]]),
                                                 axis=0)
        except IOError:
            print("ERROR: File could not be loaded")
            return

    def MakeZero(self):
        self.divisionCount = 0
        self.avgProbN = 0
        self.avgProbS = 0

    def AddAvg(self, idx):
        self.divisionCount += 1
        self.avgProbN += self.logfileData[idx, 3]
        self.avgProbS += self.logfileData[idx, 4]
    # endregion

############################################################################
# child class used for window mode
############################################################################


class WindowData(PostProcessing):
    ########################################################################
    # class constructor
    ########################################################################
    # region
    def __init__(self, logfilePath, outLogFilePath, outSummary,
                 outPrePostLog, stepSize, windowSize):
        PostProcessing.__init__(self, logfilePath, outLogFilePath,
                                outSummary, outPrePostLog)
        self.stepSize = stepSize
        self.windowSize = windowSize
    # endregion

    ########################################################################
    # public methods
    ########################################################################
    # region
    def PerformPost(self, textFileName):
        ####################################################################
        # Load the log file and convert it to a 2d array to process
        ####################################################################
        self.Textfile2Array(textFileName)
        ####################################################################
        # Perform the post-processing on the 2d array of data
        ####################################################################
        if self.windowSize > len(self.logfileData):
            print("ERROR: Size of window size not sufficient")
            return
        self.__Processing(textFileName)
        ####################################################################
        # save the results to a text file
        ####################################################################
        if (self.outPrePostLog != "NULL"):
            np.savetxt(self.outPrePostLog + textFileName[:-4]
                       + "_Pre_PostP.txt",
                       self.logfileData[:][:], fmt="%s")
        if (self.outLogFilePath != "NULL"):
            np.savetxt(self.outLogFilePath + textFileName[:-4] + "_PostW1.txt",
                       self.logfileDataPost[:][:], fmt="%s")
        ####################################################################
        # calculate the summary values for this file max prob selective
        ####################################################################
        self.CreateSummaryLine()

    def SaveSummary(self):
        np.savetxt(self.outSummary + "PostW1_summary.txt",
                   self.summary[:][:], fmt="%s")
    # endregion

    ########################################################################
    # private methods
    ########################################################################
    # region
    def __Processing(self, textFileName):
        self.logfileDataPost = np.empty((0, 6), float)
        for counter in range(0, len(self.logfileData)-self.windowSize+1,
                             self.stepSize):
            firstPos = self.logfileData[counter, 0]
            lastPos = self.logfileData[counter+self.windowSize-1, 1]
            middlePos = (firstPos+lastPos)/2
            averageProbNeutral = np.average(self.logfileData
                                            [counter:counter+self.windowSize, 3])
            averageProbSelective = np.average(self.logfileData
                                              [counter:counter+self.windowSize, 4])
            self.logfileDataPost = np.append(self.logfileDataPost,
                                             np.array([[firstPos,
                                                        lastPos,
                                                        middlePos,
                                                        averageProbNeutral,
                                                        averageProbSelective,
                                                        self.windowSize
                                                        ]]),
                                             axis=0)
    # endregion

############################################################################
# child class used for window mode based on position base pairs
############################################################################


class WindowPos(PostProcessing):
    # implement a window based approach.
    # this window based approach, should
    ########################################################################
    # class constructor
    ########################################################################
    # region
    def __init__(self, logfilePath, outLogFilePath, outSummary, 
                outPrePostLog, stepSize, windowSize):
        PostProcessing.__init__(self, logfilePath, outLogFilePath,
                                outSummary, outPrePostLog)
        self.stepSize = stepSize
        self.windowSize = windowSize
    # endregion

    ########################################################################
    # public methods
    ########################################################################
    # region
    def PerformPost(self, textFileName):
        ####################################################################
        # Load the log file and convert it to a 2d array to process
        ####################################################################
        self.Textfile2Array(textFileName)
        ####################################################################
        # Perform the post-processing on the 2d array of data
        ####################################################################
        if self.windowSize > self.logfileData[len(self.logfileData)-1, 1]:
            print("ERROR: Size of window size not sufficient")
            return
        self.__Processing(textFileName)
        ####################################################################
        # save the results to a text file
        ####################################################################
        if (self.outPrePostLog != "NULL"):
            np.savetxt(self.outPrePostLog + textFileName[:-4]
                       + "_Pre_PostW2.txt",
                       self.logfileData[:][:], fmt="%s")
        if (self.outLogFilePath != "NULL"):
            np.savetxt(self.outLogFilePath + textFileName[:-4] + "_PostW2.txt",
                       self.logfileDataPost[:][:], fmt="%s")
        ####################################################################
        # calculate the summary values for this file max prob selective
        ####################################################################
        self.CreateSummaryLine()

    def SaveSummary(self):
        np.savetxt(self.outSummary + "PostW2_summary.txt",
                   self.summary[:][:], fmt="%s")
    # endregion

    ########################################################################
    # private methods
    ########################################################################
    # region
    def __Processing(self, textFileName):
        self.logfileDataPost = np.empty((0, 6), float)
        curIdx = 0
        overallCount = 0
        # run while one whole window fits in the remainder of the data
        while self.windowSize <= (self.logfileData[len(self.logfileData)-1,
                                                   1]
                                  - self.logfileData[curIdx, 0]):
            self.MakeZero()
            # here we know the first position of that window
            firstPos = self.logfileData[curIdx, 0]
            # go through one whole window
            while self.logfileData[curIdx, 1] <= self.windowSize \
                    + (self.stepSize * overallCount):
                self.AddAvg(curIdx)
                curIdx += 1
                # check if adding 1 to current index goes out of bounds
                # if yes break out of the window loop
                if curIdx >= len(self.logfileData):
                    break
            # here we know the end position of that window
            # this is -1 because we already out
            lastPos = self.logfileData[curIdx-1, 1]
            # check if division factor equals zero
            if self.divisionCount != 0:
                # add all average values to the numpy array
                self.logfileDataPost = np.append(self.logfileDataPost,
                                                 np.array([[firstPos,
                                                            lastPos,
                                                            (firstPos +
                                                             lastPos) / 2,
                                                            self.avgProbN /
                                                            self.divisionCount,
                                                            self.avgProbS /
                                                            self.divisionCount,
                                                            self.divisionCount
                                                            ]]),
                                                 axis=0)
            # break out of the main loop if the current index is out of bounds
            if (curIdx >= len(self.logfileData)):
                break
            overallCount += 1
            value = (self.stepSize * overallCount)
            curIdx = (np.abs(self.logfileData[:, 0] - value)).argmin()


class GridSize(PostProcessing):
    ########################################################################
    # class constructor
    ########################################################################
    # region
    def __init__(self, logfilePath, outLogFilePath, outSummary, 
                outPrePostLog, gridSize, maxDist, cutoff):
        PostProcessing.__init__(self, logfilePath, outLogFilePath,
                                outSummary, outPrePostLog)
        self.gridSize = gridSize
        self.maxDist = maxDist
        self.cutoff = cutoff
    # endregion

    ########################################################################
    # public methods
    ########################################################################
    # region
    def PerformPost(self, textFileName):
        ####################################################################
        # Load the log file and convert it to a 2d array to process
        ####################################################################
        self.Textfile2Array(textFileName)
        ####################################################################
        # Perform the post-processing on the 2d array of data
        ####################################################################
        if ((self.gridSize > len(self.logfileData)) and self.cutoff):
            # if cutoff is set then take the max
            self.gridSize = len(self.logfileData) - 1
            print("WARNING: Max points taken as input")

        self.__Processing(textFileName)
        ####################################################################
        # save the results to a text file
        ####################################################################
        if (self.outPrePostLog != "NULL"):
            np.savetxt(self.outPrePostLog + textFileName[:-4]
                       + "_Pre_PostP.txt",
                       self.logfileData[:][:], fmt="%s")
        if (self.outLogFilePath != "NULL"):
            if (self.cutoff):
                np.savetxt(self.outLogFilePath + textFileName[:-4]
                           + "_PostP1.txt",
                           self.logfileDataPost[:][:], fmt="%s")
            else:
                np.savetxt(self.outLogFilePath + textFileName[:-4]
                           + "_PostP2.txt",
                           self.logfileDataPost[:][:], fmt="%s")
        ####################################################################
        # calculate the summary values for this file max prob selective
        ####################################################################
        self.CreateSummaryLine()

    def SaveSummary(self):
        if (self.cutoff):
            np.savetxt(self.outSummary + "PostP1_summary.txt",
                       self.summary[:][:], fmt="%s")
        else:
            np.savetxt(self.outSummary + "PostP2_summary.txt",
                       self.summary[:][:], fmt="%s")
    # endregion

    ########################################################################
    # private methods
    ########################################################################
    # region
    def __Processing(self, textFileName):
        self.logfileDataPost = np.empty((0, 6), float)
        # calculate the grid position element
        gridPosition = ((self.logfileData[len(self.logfileData)-1, 1] -
                         self.logfileData[0, 0])
                        / self.gridSize)
        for i in range(1, self.gridSize+1):
            self.MakeZero()
            value = gridPosition * i
            # find the closest value of the grid pos to the center value
            idx = (np.abs(self.logfileData[:, 2] - value)).argmin()
            # add the first values to the average
            self.AddAvg(idx)

            # check if the first value falls in the range
            if self.logfileData[idx, 0] < value - self.maxDist or \
                    self.logfileData[idx, 1] > value + self.maxDist:
                print("WARNING: First point already outside of range")
                firstPos = self.logfileData[idx, 0]
                lastPos = self.logfileData[idx, 1]
            else:
                # calculate to the left of the grid position
                offset = 1
                # check if first index does not get out of bounds
                if idx-offset >= 0:
                    # go to the left of the genome
                    # use start position of base pair
                    while (self.logfileData[idx-offset, 0] >
                           value-self.maxDist):
                        self.AddAvg(idx-offset)
                        offset += 1
                        if idx-offset < 0:
                            break
                # calculate the first position this is the idx - offset
                # but also - 1 because always one further then you think
                firstPos = self.logfileData[idx-(offset-1), 0]

                # calculate tot the right of the grid position
                # check if first index does not get out of bounds
                offset = 1
                if idx+offset < len(self.logfileData):
                    # go to the right of the genome
                    # use end position of base pair
                    while (self.logfileData[idx+offset, 1] <
                           value+self.maxDist):
                        self.AddAvg(idx+offset)
                        offset += 1
                        if idx+offset > len(self.logfileData)-1:
                            break
                # calculate the last position this is the idx + offset
                # but also - 1 because always one further then you think
                lastPos = self.logfileData[idx+(offset-1), 1]

            # check if division factor equals zero
            if self.divisionCount == 0:
                continue
            # add all average values to the numpy array
            self.logfileDataPost = np.append(self.logfileDataPost,
                                             np.array([[firstPos,
                                                        lastPos,
                                                        (firstPos +
                                                         lastPos) / 2,
                                                        self.avgProbN
                                                        / self.divisionCount,
                                                        self.avgProbS
                                                        / self.divisionCount,
                                                        self.divisionCount
                                                        ]]),
                                             axis=0)
    # endregion
