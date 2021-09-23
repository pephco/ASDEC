import os
import sys
import numpy as np
import re
from contextlib import redirect_stdout
import getopt

def helpPrinter():
    print("gatherResults.py -i <input directory> -o <output file> -l <chromosome length>")

def main(argv):
    inputDirectory = ''
    outputDirectory = ''
    try:
        opts, ars = getopt.getopt(argv, "hi:o:l:",
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
        elif opt in ("-l"):
            chromosomeLength = arg

    if (len(inputDirectory) == 0 or len(outputDirectory) == 0):
        print("ERROR: not all fields are filled in!")
        helpPrinter()
        sys.exit()
    
    substringAcc = ""
    substringTPR = ""
    substringTime = ""
    doneSubstring = [""]    
    file_object = open(outputDirectory, 'w')
    file_object.write("Network architecture\t\tTraining \t\tTesting \tAccuracy\tDist error\tTPR(5% FPR)\tExe time BASE\tExe time TEST\n")
    for dirname, dirs, files in os.walk(inputDirectory):
        for filename in files:
            if filename == 'acc.txt':
                with open(os.path.join(dirname, filename), 'r') as f:
                    substringAcc = dirname.rsplit('/',1)[0]
                    for line in f.readlines():
                        if "/logTraj_TEST" in line:
                            substringaccTrain = re.search("_input2/(.*?)input/", line).group(1)
                            substringaccInference = re.search("input/(.*?)/logTraj_TEST", line).group(1)
                            substringModel = re.search("_/(.*?)_input2/BASETEST", line).group(1)
                            resultsacc = np.array(re.findall("\d+\.\d+", line))
                            resultsacc = resultsacc.astype(np.float)
            elif filename == 'tprfpr.txt':
                with open(os.path.join(dirname, filename), 'r') as f:
                    substringTPR = dirname.rsplit('/',1)[0]
                    for line in f.readlines():
                        if "/logTraj_TEST" in line:
                            substringTPRTrain = re.search("_input2/(.*?)input/", line).group(1)
                            substringTPRInference = re.search("input/(.*?)/logTraj_TEST", line).group(1)
                            resultsTPR = np.array(re.findall("\d+\.\d+", line))
                            resultsTPR = resultsTPR.astype(np.float)
            elif filename == 'TimeOverview.txt':
                with open(os.path.join(dirname, filename), 'r') as f:
                    substringTime = dirname.rsplit('/',1)[0]
                    for line in f.readlines():
                        if "BASE" in line:
                            resultsBaseTime = np.array(re.findall("\d+\.\d+", line))
                            resultsBaseTime = resultsBaseTime.astype(np.float)
                        if "TEST" in line:
                            resultsTestTime = np.array(re.findall("\d+\.\d+", line))
                            resultsTestTime = resultsTestTime.astype(np.float)
            if (len(substringAcc) != 0 and len(substringTPR) != 0 and len(substringTime) != 0):
                if (not(substringAcc in doneSubstring) and not(substringTime in doneSubstring) and not(substringTPR in doneSubstring)):
                    if (substringTime == substringAcc and substringTime == substringTPR):
                        print("SAVING:")
                        print("Time File: \t" + substringTime)
                        print("accuracy File: \t" + substringAcc)
                        print("TPR File: \t" + substringTPR)
                        file_object.write(substringModel + "\t\t" + substringaccTrain + "\t\t" 
                        + substringaccInference + "\t\t"
                        + str(format(resultsacc[len(resultsacc) - 2], ".5f")) + "\t\t" 
                        + str(format(resultsacc[len(resultsacc) - 1]/float(chromosomeLength), ".5f")) + "\t\t" 
                        + str(format(resultsTPR[len(resultsTPR) - 1], ".2f")) + 
                        "\t\t" + str(format(resultsBaseTime[0], ".5f")) + 
                        "\t\t" + str(format(resultsTestTime[0], ".5f")) + "\n")
                        doneSubstring.append(substringAcc)
                    else:
                        print("ERROR: mismatch reading")
                        print("Time File: \t" + substringTime)
                        print("accuracy File: \t" + substringAcc)
                        print("TPR File: \t" + substringTPR)

             
    file_object.close()

if __name__ == "__main__":
    main(sys.argv[1:])