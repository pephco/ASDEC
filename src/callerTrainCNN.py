#!/usr/bin/python
############################################################################
# File:			callerTrainCNN.py
# Organization:	University of twente
# Group:		CAES
# Date:			16-10-2021
# Version:		2.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Calls the CNN software.
# Also provides some interfacing to explain which options are
# available.
############################################################################


# region import packages
import sys
import getopt

# import my own files
from logic import CNN
from logic import logo
from logic import str2bool
from logic import errorHandling
from logic import datatypes
# endregion


############################################################################
# Function which prints the information displayed in the terminal when
# -h is provided or nothing is provided
############################################################################


def helpPrinterCNN():
    logo.logo()
    print("callerTrainCNN.py -m <model> -d <directory> -y <imgHeight> -x <imgWidth> -b" +
          " <batchSize> -a <modelDesign>")
    print("\t -h: help option")
    print("\t -m, --model: provide the name as which the model will be saved")
    print("\t -d, --directory: give the directory where the images are stored" +
          "\n\t folders inside the directory define the classes")
    print("\t -b, --batchSize: size of the batches")
    print("\t -e, --epoch: the amount of training cycle's")
    print("\t -y, --imgHeight: height of the input images, should be the same")
    print("\t -x, --imgWidth: width of the input images, should be the same")
    print("\t -t, --threads: amount of threads used during training")
    print("\t--GPU: use GPU for training")
    print("\t--CPU: use CPU for training")
    print("\t-NS: binary classification of neutral and soft sweep")
    print("\t-NHS: multi-class classification of neutral, hard sweep and soft sweep")
    print("\t-NH: binary classification of neutral and hard sweep")
    print("\t -a, --modelDesign: name of py file where the required model is defined\n" +
        "\t !advanced option NOT REQUIRED (will default to correct model)!")


############################################################################
# Function which handles all different input arguments
############################################################################


def main(argv):
    ########################################################################
    # initialize some empty variables to store the values
    # even when no values are assigned easy to see that
    # no values where assigned
    ########################################################################
    direc = ''
    batchS = ''
    imgH = ''
    imgW = ''
    ep = ''
    mod = ''
    design = 'originalModel'
    threads = '' 
    hardware = datatypes.Hardware.CPU
    classification = datatypes.Classification.NH

    ########################################################################
    # get all the arguments from the commandline
    ########################################################################
    try:
        opts, ars = getopt.getopt(argv, "hm:d:y:x:b:e:a:t:",
                                  ["model=", "directory=", "imgHeight=",
                                   "imgWidth=", "batchSize=", "epoch=",
                                   "modelDesign=", "threads=", "GPU", "CPU",
                                   "NS", "NH", "NHS"])
    except getoptError:
        helpPrinterCNN()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            helpPrinterCNN()
            sys.exit()
        elif opt in ("-m", "--model"):
            mod = arg
        elif opt in ("-d", "--directory"):
            direc = arg
        elif opt in ("-y", "--imgHeight"):
            imgH = arg
        elif opt in ("-x", "--imgWidth"):
            imgW = arg
        elif opt in ("-b", "--batchSize"):
            batchS = arg
        elif opt in ("-e", "--epoch"):
            ep = arg
        elif opt in ("-a", "--modelDesign"):
            design = arg
        elif opt in ("-t", "--threads"):
            threads = arg
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
    # check if all parameters are filled in
    ########################################################################
    errorHandling.ErrorHandling.FieldFilledInCheck(
        direc, imgH, imgW, batchS, ep, mod, threads
    )
    errorHandling.ErrorHandling.GreaterThenZeroCheck(
        batchS, imgW, imgH, ep, threads
    )
    errorHandling.ErrorHandling.ClassificationSelected(classification)
    errorHandling.ErrorHandling.HardwareSelected(hardware)    
    if (design != "ModelDesignC3F32EL1S32_"):
        print("ADVANCED OPTION FILLED IN, MODEL SELECTED: " + str(design))
    
    ########################################################################
    # call the code which really does the work
    ########################################################################
    trainModel = CNN.Training(mod, int(float(imgH)),
                              int(float(imgW)), direc,
                              int(float(batchS)),
                              int(float(ep)),
                              str(design), int(threads),
                              hardware, classification)
    trainModel.traingModel()


if __name__ == "__main__":
    main(sys.argv[1:])
