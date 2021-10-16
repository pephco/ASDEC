#!/usr/bin/python
############################################################################
# File:			TrainCNN.py
# Organization:	University of twente
# Group:		CAES
# Date:			15-10-2021
# Version:		2.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Handles the complete training of the model including the generation
# of the ms and mssel files. This program provides a complete repoducing
# environment. Please ensure for correct working that there exists a folder
# trajectory_files which includes all needed trajectory_files. These are
# not included in the git repo due to the size.
############################################################################

# region import packages
import sys
import getopt
import subprocess
import shlex
import random
from contextlib import redirect_stdout
import time
import os
import numpy as np
import re
from subprocess import Popen, PIPE

# import my own files
from logic import datatypes
from logic import errorHandling
import callerBitmap
import callerTrainCNN
from logic import randomGenerator
from logic import str2bool
from logic import logo
# endregion

def HelpPrinterTrain():
    logo.logo()
    print("TrainCNN.py")
    print("Handles the complete training of the model including the generation")
    print("of the ms and mssel files. This program provides a complete repoducing")
    print("environment. Please ensure for correct working that there exists a folder")
    print("trajectory_files which includes all needed trajectory_files. These are")
    print("not included in the git repo due to the size or give the path to your own files.")
    print("\n")
    print("Settings for ms/mssel generation:")
    print("Options for automatic generation of ms/mssel data, if data in the")
    print("ms/mssel format is already present. Please use the -w flag and")
    print("the: -a, -b, -c, -d, -e, -f flags can be left unused.")
    print("\t-a: start ms simulation (int) (def: 0)")
    print("\t-b: end ms simulation included (int) (def: 0)")
    print("\t-c: start mssel simulation (int) (def: 0)")
    print("\t-d: end mssel simulation included (int) (def: 0)")
    print("\t-e: number of populations per ms/mssel file (int) (def: 1)")
    print("\t-f: number of individuals per population ms/mssel file (int) (def: 20)")
    print("\n")
    print("Bitmap generation settings:")
    print("The following settings consider the generation of each bitmap/image.")
    print("Please note that all settings are represented by snips/pixels.")
    print("extraction mode can be used to only take a subset of a given snips in the extraction,")
    print("with a given range (value is a single direction in snips).")
    print("Note that under normal use the -g and -k flags true and work together.")
    print("\t-g: enable window mode (bool) (def: true)")
    print("\t\t-i: window length/size (int) (def: 50)")
    print("\t\t-j: step between windows (int) (def: 1)")
    print("\t-k: enable extraction mode (bool) (def: true)")
    print("\t\t-y: position for extraction mode (float) (def: 500000)")
    print("\t\t-l: range for extraction mode (int) (def: 28)")
    print("\t-m: multiplication factor position (float) (def: 1000000)")
    print("\n")
    print("CNN train settings:")
    print("The following settings consider all settings possible for training of")
    print("a given model based on a model design.")
    print("\t-n: batch size (int) (def: 1)")
    print("\t-o: amount of epochs (int) (def: 10)")
    print("\t-p: output path + model name (string) (def: tempModel)")
    print("\t\t--force: save even if model is already present (bool) (def: false)")
    print("\n")
    print("Classification type settings (select one):")
    print("\t-NS: binary classification of neutral and soft sweep")
    print("\t-NHS: multi-class classification of neutral, hard sweep and soft sweep")
    print("\t-NH: binary classification of neutral and hard sweep")
    print("\n")
    print("Hardware to use (select one)")
    print("\t--GPU: use GPU for training")
    print("\t--CPU: use CPU for training")
    print("\n")
    print("Advanced settings !Please use with caution!:")
    print("Two advanced options are available -q considers model designs.")
    print("These designs are located in the /src/models folder please do not")
    print("specify the path to a given model and do not create sub-folders in")
    print("this folder. Only provide the name of the model design in the")
    print("/src/models folder without .py exstension.")
    print("For the -t flag please specify a path where under that path two")
    print("subfolders are located called neutral and selection.")
    print("In both these subfolders only .txt files in the ms/mssel format")
    print("should be present.")
    print("\t-q: name of py file where the required model is defined\n" +
          "\t(string) (def: ModelDesignC3F32EL1S32_)")
    print("\t-t: get raw files path (string) (def: NULL)")
    print("\n")
    print("General settings:")
    print("\t-r: Perform cleanup (bool) (def: true)")
    print("\t-z: Amount of threads used (int) (def: 5)")
    print("\n")
    print("Extra training settings:")
    print("These specify a maximal loss and mininal acc, used for rapid")
    print("retraining")
    print("\t-u: minimal accuracy (float) (def: 0)")
    print("\t-v: maximal loss (float) (def: infinite)")
    print("\t-w: amount of tries (int) (def: 1)")
    print("\n")
    print("VCF parsing settings:")
    print("\t-x: parsing vcf file memory consumption (input * 2) (float) (def: 10)")
    print("\t-X: total chromosome length (float) (def 100000)")
    print("\n")


def main(argv):
    ########################################################################
    # initialize some empty variables to store the values
    # even when no values are assigned easy to see that
    # no values where assigned
    ########################################################################
    # ms and mssel generation settings
    startMs = '0'
    endMs = '0'
    startMssel = '0'
    endMssel = '0'
    numberOfPopulations = '1'
    individuals = '20'
    # bitmap generation settings
    windowEnb = 'true'
    windowLength = '50'
    stepSize = '1'
    centerEnb = 'true'
    centerRange = '28'
    extractionPoint = '500000'
    multiplication = '1000000'
    # CNN training settings
    batchSize = '1'
    epoch = '10'
    model = 'tempModel'
    # default given in the caller of the train cnn
    design = 'ModelDesignC3F32EL1S32_'
    # general settings
    deleteWhenDone = 'true'
    rawFilesPath = ''
    force = False
    threads = '5'
    hardware = datatypes.Hardware.NULL
    classification = datatypes.Classification.NULL
    # extra training settings
    minAcc = 0
    maxLoss = sys.float_info.max
    triesCount = 1
    # vcf parsing settings
    memorySize = '10'
    chromosomeLength = '100000'
    
    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv,
                                  "ha:b:c:d:e:f:g:i:j:k:l:m:n:o:p:q:r:t:u:v:w:y:x:X:z:",
                                  ["force", "GPU", "CPU", "NS", "NH", "NHS"])
    except getoptError:
        HelpPrinterTrain()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            HelpPrinterTrain()
            sys.exit(1)
        elif opt in ("-a"):
            startMs = arg
        elif opt in ("-b"):
            endMs = arg
        elif opt in ("-c"):
            startMssel = arg
        elif opt in ("-d"):
            endMssel = arg
        elif opt in ("-e"):
            numberOfPopulations = arg
        elif opt in ("-f"):
            individuals = arg
        elif opt in ("-g"):
            windowEnb = arg
        elif opt in ("-i"):
            windowLength = arg
        elif opt in ("-j"):
            stepSize = arg
        elif opt in ("-k"):
            centerEnb = arg
        elif opt in ("-l"):
            centerRange = arg
        elif opt in ("-m"):
            multiplication = arg
        elif opt in ("-n"):
            batchSize = arg
        elif opt in ("-o"):
            epoch = arg
        elif opt in ("-p"):
            model = arg
        elif opt in ("-q"):
            design = arg
        elif opt in ("-r"):
            deleteWhenDone = arg
        elif opt in ("-t"):
            rawFilesPath = arg
        elif opt in ("-u"):
            minAcc = float(arg)
        elif opt in ("-v"):
            maxLoss = float(arg)
        elif opt in ("-w"):
            triesCount = int(arg)
        elif opt in ("-y"):
            extractionPoint = arg
        elif opt in ("-x"):
            memorySize = arg
        elif opt in ("-X"):
            chromosomeLength = arg
        elif opt in ("-z"):
            threads = arg
        elif opt in ("--force"):
            force = True
        elif opt in ("--CPU"):
            errorHandling.ErrorHandling.HardwareCheck(hardware)
            hardware = datatypes.Hardware.CPU
        elif opt in ("--GPU"):
            errorHandling.ErrorHandling.HardwareCheck(hardware)
            hardware = datatypes.Hardware.GPU
        elif opt in ("--NS"):
            errorHandling.ErrorHandling.ClassificationCheck(classification)
            classification = datatypes.Classification.NS
        elif opt in ("--NH"):
            errorHandling.ErrorHandling.ClassificationCheck(classification)
            classification = datatypes.Classification.NH
        elif opt in ("--NHS"):
            errorHandling.ErrorHandling.ClassificationCheck(classification)
            classification = datatypes.Classification.NHS
    
    ########################################################################
    # check if some options are filled in
    ### time ###
    startTime = time.time()
    ########################################################################
    # check if there is enough data to perform the inference
    errorHandling.ErrorHandling.InputDataCheck(startMs, endMs, startMssel, endMssel, rawFilesPath)
    errorHandling.ErrorHandling.TryCountCheck(triesCount)
    errorHandling.ErrorHandling.ThreadNumberCheck(threads)
    errorHandling.ErrorHandling.ModelExistsCheck(model, force)    
    if(len(rawFilesPath) == 0):
        errorHandling.ErrorHandling.TrajectoryExistsFolderCheck()
    errorHandling.ErrorHandling.ClassificationSelected(classification)
    errorHandling.ErrorHandling.HardwareSelected(hardware)    
    ########################################################################
    # run all the scripts and python code
    # setup the file structure
    ########################################################################
    print("start running all scripts and timer")
    print("generate random folder name")
    folderName = 'out/outTrain_' + str(randomGenerator.id_generator())
    print("folder name: " + str(folderName))

    # create out folder
    subprocess.call(shlex.split('./src/scripts/makeFolder.sh' +
                                ' -d out '))

    # call the cleaning script
    subprocess.call(shlex.split(
        './src/scripts/cleanCompleteTrain.sh' +
        ' -d ' + str(folderName)))
    ########################################################################
    # If no raw files are already given generate them
    ### time ###
    timeInitialSetup = time.time() - startTime
    startTime = time.time()
    ########################################################################
    if (len(rawFilesPath) == 0):
        # call the ms/mssel generation script
        subprocess.call(shlex.split('./src/scripts/dataGeneration.sh' +
                                    ' -s ' + str(int(startMs)) +
                                    ' -e ' + str(int(endMs)) +
                                    ' -b ' + str(int(startMssel)) +
                                    ' -f ' + str(int(endMssel)) +
                                    ' -i ' + str(int(numberOfPopulations)) +
                                    ' -c ' + str(int(individuals)) +
                                    ' -d ' + str(folderName) +
                                    ' -t ' + str(int(threads))))
        rawFilesPath = folderName + "/raw"           
    
    ########################################################################
    # Generate the images
    ### time ###
    timeDataGeneration = time.time() - startTime
    startTime = time.time()
    ########################################################################
    filesToRun = [[]]
    classesFound = []
    processes = [[]]
    print("Start conversion to bitmaps")
    # explore the folder for all files to run
    with os.scandir(str(rawFilesPath)) as folder:
        for subfolder in folder:
            tempFiles = []
            if subfolder.is_dir():
                classesFound.append(str(subfolder.name))
                for textFile in subfolder:
                    if textFile.is_file():
                        tempFiles.append(str(textFile.path))
            filesToRun.append(tempFiles)
    errorHandling.ErrorHandling.ClassesCheck(classesFound, classification.fromStr)
    classIndex = 0
    for folders in filesToRun:
        startedIndex = 0
        for files in folders:
            startedIndex += 1
            p = subprocess.Popen("python3 src/callerBitmap.py" + ' -i ' + files +
                            ' -o ' + str(folderName) +
                            '/img/' + classification.fromStr[classIndex] + '/img' + str(startedIndex) + "_" +
                            ' -w ' + str(windowEnb) +
                            ' -l ' + str(windowLength) +
                            ' -s ' + str(stepSize) +
                            ' -c ' + str(centerEnb) +
                            ' -z ' + str(centerRange) +
                            ' -m ' + str(multiplication) +
                            ' -p ' + str(extractionPoint) +
                            ' -x ' + str(memorySize) 
                            , stdout=subprocess.PIPE, shell=True)
            processes.append(p)
            if int(threads) <= startedIndex:
                startedIndex = 0
                for p in processes:
                    if p.wait() != 0:
                        print("ERROR: There was an error in thread timing")
        if (startedIndex == 0):
            print("WARNING: No txt files found do in " + str(folders))
                    
    # open a single file to get the number of individuals
    if (len(filesToRunNeutral) > 0):
        getIndividuals = filesToRunNeutral[0]
    elif (len(filesToRunSelection) > 0):
        getIndividuals = filesToRunSelection[0]
    else:
        getIndividuals = ""
        print("ERROR: No files found")
        sys.exit(1)
    
    if getIndividuals.endswith(".vcf"):
        getIndividuals = getIndividuals + ".ms"
    msFile = open(getIndividuals, 'r')
    for lineIndex, line in enumerate(msFile):
        if lineIndex == 0:
            individuals = str([
                int(lineIndex) for lineIndex in line.split() if
                lineIndex.isdigit()][0])
        break
    msFile.close()
    ########################################################################
    # Train the model
    ### time ###
    timeImageGeneration = time.time() - startTime
    startTime = time.time()
    ########################################################################
    
    # call the cnn
    for i in range(triesCount):
        callerTrainCNN.main(['-m' + str(model),
                             '-d' + str(folderName) + '/img/',
                             '-b' + str(batchSize),
                             '-e' + str(epoch),
                             '-y' + str(individuals),
                             '-x' + str(windowLength),
                             '-a' + str(design),
                             '-t' + str(threads),
                             inputLineTraining])
        # check the acc
        openfile = open(str(model) + "/TrainResultsAcc.txt", 'r')
        for lineIndex, line in enumerate(openfile):
            if lineIndex == int(epoch)-1:
                finalAcc = np.array(re.findall("\d+\.\d+", line))
                finalAcc = finalAcc.astype(np.float)
                break
        openfile.close()
        # check the loss
        openfile = open(str(model) + "/TrainResultsLoss.txt", 'r')
        for lineIndex, line in enumerate(openfile):
            if lineIndex == int(epoch)-1:
                finalLoss = np.array(re.findall("\d+\.\d+", line))
                finalLoss = finalLoss.astype(np.float)
                break
        openfile.close()
        # performs checks
        print(finalAcc)
        print(finalLoss)
        if (finalAcc[1] >= minAcc and finalAcc[2] >= minAcc and
            finalLoss[1] <= maxLoss and finalLoss[2] <= maxLoss):
            print("Model is within requirements")
            break
        
    ########################################################################
    # Perform the clean up
    ### time ###
    timeTrain = time.time() - startTime
    startTime = time.time()
    ########################################################################

    # call the cleaning script
    if(str2bool.str2bool(deleteWhenDone)):
        print("cleaning up the folder and deleting it")
        subprocess.call(shlex.split(
            './src/scripts/deleteFolder.sh' +
            ' -d ' + str(folderName)))

    ########################################################################
    # Save all logs and the script is completed
    ### time ###
    timeCleanUp = time.time() - startTime
    ########################################################################

    print("No more measurements being done")
    print("Saving execution time data")
    # save terminal command used for creation
    with open((model + "/CommandLine.txt"), 'w') as f:
        with redirect_stdout(f):
            print("-a " + str(startMs))
            print("-b " + str(endMs))
            print("-c " + str(startMssel))
            print("-d " + str(endMssel))
            print("-e " + str(numberOfPopulations))
            print("-f " + str(individuals))
            print("-g " + str(windowEnb))
            print("-i " + str(windowLength))
            print("-j " + str(stepSize))
            print("-k " + str(centerEnb))
            print("-l " + str(centerRange))
            print("-m " + str(multiplication))
            print("-n " + str(batchSize))
            print("-o " + str(epoch))
            print("-p " + str(model))
            print("-q " + str(design))
            print("-r " + str(deleteWhenDone))
            print("-t " + str(rawFilesPath))
            print("-y " + str(extractionPoint))
            print("-x " + str(memorySize))
            print("-X " + str(chromosomeLength))
            print("-z " + str(threads))
            if force:
                print("--force")
            if CPU:
                print("--CPU")
            if GPU:
                print("--GPU")

    totalTime = (timeInitialSetup + timeDataGeneration + timeImageGeneration
                 + timeTrain + timeCleanUp)

    with open((model + "/TimingResults.txt"), 'w') as f:
        with redirect_stdout(f):
            print("Time summary in seconds\n")
            print("Initial setup time------------:\t%.5f" %
                  timeInitialSetup)
            print("Data generation time----------:\t%.5f" %
                  timeDataGeneration)
            print("Bitmap generation time--------:\t%.5f" %
                  timeImageGeneration)
            print("Total training time-----------:\t%.5f" %
                  timeTrain)
            print("Total clean up time-----------:\t%.5f" %
                  timeCleanUp)
            print("Total Time -------------------:\t%.5f" %
                  totalTime)

    print("completed running all scripts")

if __name__ == "__main__":
    main(sys.argv[1:])
