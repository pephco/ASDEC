import os
import sys
import numpy as np
import re
from contextlib import redirect_stdout
import getopt

def helpPrinter():
    print("gatherModel.py -i <input directory> -o <output file>")

def main(argv):
    inputDirectory = ''
    outputDirectory = ''
    try:
        opts, ars = getopt.getopt(argv, "hi:o:",
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

    if (len(inputDirectory) == 0 or len(outputDirectory) == 0):
        print("ERROR: not all fields are filled in!")
        helpPrinter()
        sys.exit()
    
    substringAcc = ""
    substringLoss = ""
    substringTime = ""
    doneSubstring = [""]
    file_object = open(outputDirectory, 'w')
    file_object.write("Network architecture\tTraining  \t\tAcc train\tAcc val\t\tLoss train\tLoss val\tTotal time\n")
    for dirname, dirs, files in os.walk(inputDirectory):
        for filename in files:
            if filename == 'TrainResultsAcc.txt':
                with open(os.path.join(dirname, filename), 'r') as f:
                    substringAcc = dirname
                    substringAccArc = re.search("models/(.*?)input2", substringAcc).group(1)
                    substringAccTrain = substringAcc.split("_input2/",1)[1] 
                    for line in f.readlines():
                        tempacc = np.array(re.findall("\d+\.\d+", line))
                        tempacc = tempacc.astype(np.float)
                        if tempacc[0] == 5.0:
                            resultsacc = tempacc
            elif filename == 'TrainResultsLoss.txt':
                with open(os.path.join(dirname, filename), 'r') as f:
                    substringLoss = dirname
                    for line in f.readlines():
                        temploss = np.array(re.findall("\d+\.\d+", line))
                        temploss = temploss.astype(np.float)
                        if temploss[0] == 5.0:
                            resultsloss = temploss
            elif filename == 'TimingResults.txt':
                with open(os.path.join(dirname, filename), 'r') as f:
                    substringTime = dirname
                    for line in f.readlines():
                        if "Total Time" in line:
                            resultsTotalTime = np.array(re.findall("\d+\.\d+", line))
                            resultsTotalTime = resultsTotalTime.astype(np.float)
                            
            if (len(substringAcc) != 0 and len(substringLoss) != 0 and len(substringTime) != 0):
                if (not(substringAcc in doneSubstring) and not(substringTime in doneSubstring) and not(substringLoss in doneSubstring)):
                    if (substringTime == substringAcc and substringTime == substringLoss):
                        print("SAVING:")
                        print("Time File: \t" + substringTime)
                        print("accuracy File: \t" + substringAcc)
                        print("Loss File: \t" + substringLoss)
                        file_object.write(substringAccArc + "\t" + substringAccTrain + "  \t" 
                        + str(format(resultsacc[1], ".5f")) + "\t\t" 
                        + str(format(resultsacc[2], ".5f")) + "\t\t" 
                        + str(format(resultsloss[1], ".5f")) + "\t\t"
                        + str(format(resultsloss[2], ".5f")) + "\t\t"
                        + str(format(resultsTotalTime[0], ".5f")) + "\n")
                        doneSubstring.append(substringAcc)
                    else:
                        print("ERROR: mismatch reading")
                        print("Time File: \t" + substringTime)
                        print("accuracy File: \t" + substringAcc)
                        print("Loss File: \t" + substringLoss)
                        helpPrinter()
                        sys.exit()                    
                                   
    file_object.close()

if __name__ == "__main__":
    main(sys.argv[1:])