#!/usr/bin/python
############################################################################
# File:			LoadCNN.py
# Organization:	University of twente
# Group:		CAES
# Date:			31-07-2021
# Version:		1.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Handles the complete loading of the model inclduing the generation
# of the ms and mssel files. This program provides a complete repoducing
# environment. Please ensure for correct working that there exists a folder
# trajectory_files which includes all needed trajectory files. these are
# not included in the git repo due to the size.
############################################################################

# region import packages
import sys
import getopt
import subprocess
import shlex
from contextlib import redirect_stdout
import time
import os

# import my own files
import callerBitmap
import callerLoadCNN
from logic import randomGenerator
import callerPostProcessing
from logic import str2bool
from logic import logo
from logic import vcfConversion
# endregion


def HelpPrinterLoad():
    logo.logo()
    print("LoadCNN.py")
    print("Handles the complete loading of the model inclduing the generation")
    print("of the ms and mssel files. This program provides a complete repoducing")
    print("environment. Please ensure for correct working that there exists a folder")
    print("trajectory_files which includes all needed trajectory files. these are")
    print("not included in the git repo due to the size.")
    print("\n")
    print("CNN load settings:")
    print("Provide the path to the model, including the model name")
    print("\t-n: model path + name (string) (def: NULL)")
    print("\n")
    print("Bitmap generation settings:")
    print("The following settings consider the generation of each bitmap/image.")
    print("Please note that all settings are represented by snips/pixels.")
    print("\t-m: multiplication factor position (float) (def: 1000000)")
    print("Post processing settings:")
    print("To perform post processing please provide a path in the form of a folder where")
    print("the results can be saved only the -o flag is forced.")
    print("\t-o: directory save post log files (string) (def: NULL !not saved!)")
    print("\t-q: mode (int) (see below) (def: 3)")
    print("\t\tMode 1: Window based on entries in the file")
    print("\t\t\t-r: stepsize in entries in the file (def: 4000)")
    print("\t\t\t-s: windowsize in entries in the file (def: 10000)")
    print("\t\tMode 2: Window based on position")
    print("\t\t\t-r: stepsize in position (def: 4000)")
    print("\t\t\t-s: windowsize in position (def: 10000)")
    print("\t\tMode 3: Grid normal mode")
    print("\t\t\t-r: gridsize in interger value (if set to zero just " +
          "\t\n\t\t\t take the amount of entries in the file) (def: 4000)")
    print("\t\t\t-s: max distance range in position (def: 10000)")
    print("\t\tMode 4: Grid no max size check (always enforces grid size)")
    print("\t\t\t-r: gridsize in interger value (def: 4000)")
    print("\t\t\t-s: max distance range (def: 10000)")
    print("\n")
    print("Settings general:")
    print("These settings are required to suite the hardware")
    print("For the -w flag please specify a path where under that path are one")
    print("or more subfolders are located (foldername letters and numbers).")
    print("In all these subfolders only .txt files in the ms/mssel format")
    print("should be present.")
    print("\t-t: amount of threads (def: 1)")
    print("\t-u: Perform cleanup (bool) (def: false)")
    print("\t-v: amount of steps done per thread (def: 5)")
    print("\t-w: get raw files path (string) (def: NULL)")
    print("\t--GPU: use GPU for inference")
    print("\t--CPU: use CPU for inference")
    print("\n")
    print("\n")
    print("!The following options are for advanced users only and enables search mode!")
    print("\t--search: enables the search mode features")
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
    print("\t-f: number of individuals per population ms/mssel file (int) (def: required by model)")
    print("\n")
    print("Bitmap generation settings:")
    print("\t-g: enable window mode (bool) (def: true)")
    print("\t\t-i: window length/size (int) (def: required by model)")
    print("\t\t-j: step between windows (int) (def: 1)")
    print("\t-k: enable extraction mode (bool) (def: false)")
    print("\t\t-y: position for extraction mode (float) (def: 500000)")
    print("\t\t-l: range for extraction mode (int) (def: 28)")
    print("\n")
    print("Post processing settings:")
    print("To save all files in a standard file structure under the path of the")
    print("summary directory set one or both the -x and -o flag to true.")
    print("This will save them both in a file structure under the -p directory")
    print("\t-p: directory save summary files (string) (def: NULL !not saved!)")
    print("\t-x: directory save pre-post log files (string) (def: NULL !not saved!)")
    print("\n")
    print("VCF parsing settings:")
    print("\t-z: parsing vcf file memory consumption (input * 2) (float) (def: 10)")
    print("\t-Z: total chromosome length (float) (def 100000)")
    
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
    numberOfPopulations = 1
    individuals = 'NULL'
    # bitmap generation settings
    windowEnb = 'true'
    windowLength = 'NULL'
    stepSize = '1'
    centerEnb = 'false'
    centerRange = '28'
    extractionPoint = '500000'
    multiplication = '1000000'
    # CNN load settings
    model = 'NULL'
    # Post processing settings
    logPost = 'NULL'
    logPrePost = 'NULL'
    logSummary = 'NULL'
    mode = '3'
    parama = '4000'
    paramb = '10000'
    # general settings
    threads = 1
    deleteWhenDone = 'false'
    stepsPerThread = '5'
    rawFilesPath = ''
    search = False
    setSearchParameter = False
    CPU = False
    GPU = False
    # vcf parsing settings
    memorySize = '10'
    chromosomeLength = '100000'

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv,
                                  "ha:b:c:d:e:f:g:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z:Z:", 
                                  ["search", "GPU", "CPU"])
    except getoptError:
        HelpPrinterLoad()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            HelpPrinterLoad()
            sys.exit(1)
        elif opt in ("-a"):
            startMs = arg
            setSearchParameter = True
        elif opt in ("-b"):
            endMs = arg
            setSearchParameter = True
        elif opt in ("-c"):
            startMssel = arg
            setSearchParameter = True
        elif opt in ("-d"):
            endMssel = arg
            setSearchParameter = True
        elif opt in ("-e"):
            numberOfPopulations = int(arg)
            setSearchParameter = True
        elif opt in ("-f"):
            individuals = arg
            setSearchParameter = True
        elif opt in ("-g"):
            windowEnb = arg
            setSearchParameter = True
        elif opt in ("-i"):
            windowLength = arg
            setSearchParameter = True
        elif opt in ("-j"):
            stepSize = arg
            setSearchParameter = True
        elif opt in ("-k"):
            centerEnb = arg
            setSearchParameter = True
        elif opt in ("-l"):
            centerRange = arg
            setSearchParameter = True
        elif opt in ("-p"):
            logSummary = arg
            setSearchParameter = True
        elif opt in ("-x"):
            logPrePost = arg
            setSearchParameter = True
        elif opt in ("-y"):
            setSearchParameter = True
            extractionPoint = arg
        elif opt in ("-m"):
            multiplication = arg
        elif opt in ("-n"):
            model = arg
        elif opt in ("-o"):
            logPost = arg
        elif opt in ("-q"):
            mode = arg
        elif opt in ("-r"):
            parama = arg
        elif opt in ("-s"):
            paramb = arg
        elif opt in ("-t"):
            threads = int(arg)
        elif opt in ("-u"):
            deleteWhenDone = arg
        elif opt in ("-v"):
            stepsPerThread = arg
        elif opt in ("-w"):
            rawFilesPath = arg
        elif opt in ("-z"):
            memorySize = arg
        elif opt in ("-Z"):
            chromosomeLength = arg
        elif opt in ("--search"):
            search = True
        elif opt in ("--CPU"):
            CPU = True
        elif opt in ("--GPU"):
            GPU = True
        
    ########################################################################
    # check if options are filled in correctly
    ### time ###
    if(logSummary != "NULL"):
        completeTime = time.time()
        startTime = time.time()
    ########################################################################
    # check if there is enough data to perform the inference
    if ((int(startMs) == 0 and int(endMs) == 0 and int(startMssel) == 0
        and int(endMssel) == 0 and len(rawFilesPath) == 0) or 
        (int(startMs) > int(endMs) or int(startMssel) > int(endMssel))):
        HelpPrinterLoad()
        print("ERROR: Not enough data to perform inference")
        sys.exit(1)
    
    # model not specified
    if (str(model) == "NULL"):
        print("ERROR: Model not specified")
        sys.exit(1)
        
    # nothing is being saved
    if (str(logPrePost) == "NULL" and str(logSummary) == "NULL" 
        and str(logPost) == "NULL"):
        print("ERROR: No saving location given")
        sys.exit(1)
    
    # check if search mode items are used without search mode enabled
    if (setSearchParameter and not search):
        print("ERROR: When you want to use search mode add --search")
        sys.exit(1)
    
    # check if the trajectory folder exists before running the code
    if (int(startMssel) > 0):
        if (not os.path.exists("trajectory_files/")):
            print("ERROR: no folder called trajectory files, please")
            print("run: ./tools/setupTrajectoryFiles.sh")
            sys.exit(1)
    
    # Check hardware selection
    if (CPU and GPU == False):
        inputLineTraining = "--CPU"
    elif (CPU == False and GPU):
        inputLineTraining = "--GPU"
    else:
        print("ERROR: Selected none or multiple hardware settings")
        print("only use one --GPU or --CPU")
        sys.exit(1)
    
    ########################################################################
    # read the required information from the commandline
    # if commands are overwritten using save mode they are not loaded
    ########################################################################
    print("Reading the commandline arguments from the model")
    commandLineModel = open(str(model) + '/CommandLine.txt', 'r')
    for lineIndex, line in enumerate(commandLineModel):
        # find the -f line, which tells us the height of the image
        if (individuals == "NULL"):
            if line.find('-f ') != -1:
                individuals = str([int(lineIndex)
                               for lineIndex in line.split()
                               if lineIndex.isdigit()][0])
        # find the width of the image from the command line log -i flag
        if (windowLength == "NULL"):
            if line.find('-i ') != -1:
                windowLength = str([int(lineIndex)
                               for lineIndex in line.split()
                               if lineIndex.isdigit()][0])
        if lineIndex > 25:
            print("ERROR: Problem with commandline log of model")
            sys.exit(1)    
    commandLineModel.close()        
    ########################################################################
    # run all the scripts and python code
    # setup the file structure
    # check the corresponding thread count
    ########################################################################
    print("start running all scripts and timer")
    print("generate random folder name")
    folderName = 'out/outLoad_' + str(randomGenerator.id_generator())
    print("folder name: " + str(folderName))

    # create out folder
    subprocess.call(shlex.split('./src/scripts/makeFolder.sh' +
                                ' -d out '))

    # call the cleaning script
    subprocess.call(shlex.split('./src/scripts/cleanCompleteLoad.sh' +
                                ' -t ' + str(threads) +
                                ' -d ' + str(folderName)))

    # call the seperate creation of the info file within the
    # designated location for saving the info of the run
    if(logSummary != "NULL"):
        print("create a sub-folder if not already done to save info")
        subprocess.call(shlex.split(
            './src/scripts/makeInfoFolder.sh' +
            ' -d ' + str(logSummary) +
            ' -t ' + str(threads)))
        if(str2bool.str2bool(logPrePost)):
            logPrePost = str(logSummary) + "preLog/"
        if(str2bool.str2bool(logPost)):
            logPost = str(logSummary) + "postLog/"
    else:
        print("no summary saving location defined so also no commandline and time saving")
        
    ########################################################################
    # if desired create the ms/mssel files
    if(logSummary != "NULL"):
        ### time ###
        timeInitialSetup = time.time() - startTime
        # start a new timer to determine the time took for writing
        startTime = time.time()
        # write the file so that later it can be appended on in the
        # other blocks, this will create a bit more overhead, because
        # the file must be openend and closed multiple times
        with open((logSummary + 'info/TimeOverview.txt'), 'w') as f:
            with redirect_stdout(f):
                print("Time summary in seconds")
                print("Complete program\n")
                print("Initial setup time------------:\t%.5f" %
                      timeInitialSetup)
                print("Write time to file------------:\t%.5f" %
                      (time.time() - startTime))
        startTime = time.time()
        ############
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
                                    ' -t ' + str(threads)))
        rawFilesPath = folderName + "/raw"

    ########################################################################
    # Perform inference on all files present in 
    if(logSummary != "NULL"):
        ### time ###
        timeDataGeneration = time.time() - startTime
        # start a new timer to determine the time took for writing
        startTime = time.time()
        # from this point on it will be appended to the existing file
        with open((logSummary + 'info/TimeOverview.txt'), 'a') as f:
            with redirect_stdout(f):
                print("Data generation time----------:\t%.5f" %
                      timeDataGeneration)
                print("Write time to file------------:\t%.5f" %
                      (time.time() - startTime))             
        startTime = time.time()
        ############
    ########################################################################
    filesToRun = []
    if ("." in rawFilesPath):
        filesToRun.append(str(rawFilesPath))
    else:
        with os.scandir(str(rawFilesPath)) as folder:
            for subfolder in folder:
                if subfolder.is_dir():
                    with os.scandir(str(subfolder.path)) as content:
                        for file in content:
                            if file.is_file():
                                filesToRun.append(str(file.path))
                elif subfolder.is_file():
                    filesToRun.append(str(subfolder.path))
    if (len(filesToRun) == 0):
        print("ERROR: No files to run")
        sys.exit(1)
    
    i = 0
    for filesFound in filesToRun:
        if vcfConversion.vcfConversion(rawFilesPath, chromosomeLength, memorySize):
            filesFound = filesFound + ".ms"
        fileName = filesFound
        while True:
            if (not "/" in fileName):
                break
            fileName = fileName.split("/",1)[-1]
        print("\n------STARTED RUNNING " + fileName + "------\n")
        # read the first line of the file to get some information
        openfile = open(filesFound, 'r')
        for lineIndex, line in enumerate(openfile):
            if lineIndex == 0:
                fileInformation = [
                    int(lineIndex) for lineIndex in line.split() if
                    lineIndex.isdigit()]
                if (line.find('mbs') != -1):
                    numberOfPopulations = fileInformation[len(fileInformation)-1]
                elif (line.find('ms') != -1 or line.find('mssel') != -1 or line.find('msHOT') != -1 ):
                    numberOfPopulations = fileInformation[1]
                else:
                    print("not supported software package")
                    return
                break
        openfile.close()
        # set the amount of populations based on the file
        # information.
        # numberOfPopulations = int(fileInformation[1])
        # if the amount of individuals is different in the
        # file from the amount used by the model training
        # the image size is not equal and not possible
        if (int(individuals) != int(fileInformation[0])):
            print("ERROR: Amount of individuals not correct")
            sys.exit(1)
        # check thread settings
        tempThreads = threads
        print("check if thread set are valid")
        if (tempThreads > numberOfPopulations):
            tempThreads = numberOfPopulations
        # call the generate script which handles all parallel parts
        # generate the bitmaps and input the bitmaps into a CNN
        subprocess.call(shlex.split(
            './src/scripts/pipelineLoad.sh' +
            ' -a ' + str(int(tempThreads)) +
            ' -b ' + filesFound +
            ' -c ' + fileName + '_IMAGE_' + str(i) +
            ' -d ' + str(windowEnb) +
            ' -e ' + str(windowLength) +
            ' -f ' + str(stepSize) +
            ' -g ' + str(centerEnb) +
            ' -i ' + str(centerRange) +
            ' -j ' + str(multiplication) +
            ' -k ' + str(model) +
            ' -l ' + str(individuals) +
            ' -m ' + '_' + fileName[:-4] + '_' +
            ' -n ' + str(numberOfPopulations) +
            ' -o ' + str(folderName) +
            ' -p ' + str(logPost) +
            ' -q ' + str(mode) +
            ' -r ' + str(parama) +
            ' -s ' + str(paramb) +
            ' -t ' + str(logSummary) +
            ' -u ' + str(stepsPerThread) +
            ' -x ' + str(logPrePost) + 
            ' -y ' + str(extractionPoint) +
            ' -z ' + str(memorySize) + 
            ' -Z ' + str(chromosomeLength) +
            ' -X ' + str(inputLineTraining)))

        if(logSummary != "NULL"):
            ### time ###
            timeProcess = time.time() - startTime
            # start a new timer to determine the time took for writing
            startTime = time.time()
            # from this point on it will be appended to the existing file
            with open((logSummary + 'info/TimeOverview.txt'), 'a') as f:
                with redirect_stdout(f):
                    print(str(fileName) + " number " + str(i) + " full process--------:\t%.5f" %
                          timeProcess)
                    print("Write time to file------------:\t%.5f" %
                          (time.time() - startTime))
            startTime = time.time()
            ############
        i += 1

    ########################################################################
    # Perform the cleanup
    ########################################################################
    if (str2bool.str2bool(deleteWhenDone)):
        print("cleaning up the folder and deleting it")
        subprocess.call(shlex.split(
            './src/scripts/deleteFolder.sh' +
            ' -d ' + str(folderName)))
    
    ########################################################################
    # Save the commandline arguments used for generation
    if(logSummary != "NULL"):
        ### time ###
        timeCleanUp = time.time() - startTime
        # start a new timer to determine the time took for writing
        startTime = time.time()
        # from this point on it will be appended to the existing file
        with open((logSummary + 'info/TimeOverview.txt'), 'a') as f:
            with redirect_stdout(f):
                print("Total clean up time-----------:\t%.5f" %
                      timeCleanUp)
                print("Write time to file------------:\t%.5f" %
                      (time.time() - startTime))
                print("Total time--------------------:\t%.5f" %
                      (time.time() - completeTime))
        ############
    ########################################################################
        # save terminal command used for creation
        with open((logSummary + 'info/CommandLine.txt'), 'w') as f:
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
                print("-n " + str(model))
                print("-o " + str(logPost))
                print("-p " + str(logSummary))
                print("-q " + str(mode))
                print("-r " + str(parama))
                print("-s " + str(paramb))
                print("-t " + str(threads))
                print("-u " + str(deleteWhenDone))
                print("-v " + str(stepsPerThread))
                print("-w " + str(rawFilesPath))
                print("-x " + str(logPrePost))
                print("-y " + str(extractionPoint))
                print("-z " + str(memorySize))
                print("-Z " + str(chromosomeLength))
                if search:
                    print("--search")
                if CPU:
                    print("--CPU")
                if GPU:
                    print("--GPU")
    print("completed running all scripts")

if __name__ == "__main__":
    main(sys.argv[1:])
