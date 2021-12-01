############################################################################
# File:			    CNN.py
# Organization:		University of twente
# Group:		    CAES
# Date:			    31-07-2021
# Version:		    1.0.0
# Author:		    Matthijs Souilljee, s2211246
# Education:	  	EMSYS msc.
############################################################################
# Convolutional Neural Network build for to distinct two classes of data.
# On the one hand neutral data and on the hand selective regions.
# Code makes use of Tensorflow in combination with Keras.
############################################################################


# region import packages
from PIL.Image import HAMMING
from tensorflow.keras.models import Sequential
import numpy as np
import os
import tensorflow as tf
import sys
import math

from logic.datatypes import Hardware
from logic.datatypes import Classification
from logic.errorHandling import ErrorHandling

from tensorflow import keras
from tensorflow.keras import (layers, models, activations,
                              optimizers, regularizers)
from contextlib import redirect_stdout
# endregion

############################################################################
# parent class for the training and pretrained child classes
# Contains a constructor that are needed by both the training
# algorithm and the model that loads the corresponding CNN.
#
# This class is not to be used directly, but rather to be used
# by the child classes
############################################################################


class CNN:

    ########################################################################
    # class constructor
    ########################################################################
    # region
    def __init__(self, modelName, directory, threads, hardware, classification):
        tf.config.threading.set_intra_op_parallelism_threads(math.floor(int(threads)/2))
        tf.config.threading.set_inter_op_parallelism_threads(math.ceil(int(threads)/2))
        self.modelName = modelName
        self.directory = directory
        self.__CheckDevice(hardware)
        self.classification = classification
    # endregion
    
    ########################################################################
    # private methods
    ########################################################################
    # region
    def __CheckDevice(self, hardware):
        print("Checking installed devices")
        CPUDevices = tf.config.list_logical_devices('CPU')
        GPUDevices = tf.config.list_logical_devices('GPU')
        try:
            if hardware == Hardware.CPU and len(CPUDevices) > 0:
                self.useDevice = '/CPU:0'
            elif hardware == Hardware.GPU and len(GPUDevices) > 0:
                print("RUNNING ON GPU")
                self.useDevice = '/GPU:0'
            else:
                print("ERROR: Hardware device not found")
                sys.exit(1)
        except:
            print("ERROR: Hardware device not correctly set")
            sys.exit(1)
        print("CPU devices: ", CPUDevices)
        print("GPU devices: ", GPUDevices)
        print("Selected device: ", self.useDevice)
    # endregion

############################################################################
# child class used for training the model
#
# This class contains all needed blocks for training a model. To use it
# please use the corresponding caller.
############################################################################


class Training(CNN):
    ########################################################################
    # class constructor
    ########################################################################
    # region
    def __init__(self, modelName, imgHeight, imgWidth, directory, 
                batch_size, epochs, modelDesignName, threads, 
                hardware, classification):
        CNN.__init__(self, modelName, directory, threads, hardware, classification)
        self.batch_size = batch_size
        self.epochs = epochs
        self.modelName = modelName
        self.imgHeight = imgHeight
        self.imgWidth = imgWidth
        self.__setDataTrain()
        self.__setDataVal()
        self.__classCheck()
        # the same as: from models import originalModel as modelDesign
        self.modelDesign = getattr(__import__("models",
                                              fromlist=[
                                                  str(modelDesignName)]),
                                   str(modelDesignName))
    # endregion

    ########################################################################
    # public methods
    ########################################################################
    # region
    def traingModel(self):
        normalization_layer = layers.experimental.preprocessing.Rescaling(scale=1./255)
        self.train_ds = self.train_ds.map(lambda x, y: (normalization_layer(x), y))
        self.val_ds = self.val_ds.map(lambda x, y: (normalization_layer(x), y))
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        self.train_ds = self.train_ds.cache().shuffle(1000).\
            prefetch(buffer_size=AUTOTUNE)
        self.val_ds = self.val_ds.cache().prefetch(buffer_size=AUTOTUNE)
        for image_batch, labels_batch in self.train_ds:
            sizeImage = image_batch.shape
            print(sizeImage)
            print(labels_batch.shape)
            break
            
        # tensorboard is really nice for looking back at models that are already trained
        tensorboard_callback = tf.keras.callbacks.TensorBoard(self.modelName + "/tensorBoard")
        
        # call the model present in a different python file
        # This step includes the compiling and fitting of the model design
        with tf.device(self.useDevice):
            self.model = self.modelDesign.model(
                len(Classification.classStr(self.classification)), sizeImage)
        
            self.history = self.model.fit(
                self.train_ds,
                validation_data=self.val_ds,
                verbose=1,
                epochs=self.epochs,
                callbacks=[tensorboard_callback]
                )
                
        # give a summary of the model in the terminal
        self.model.summary()

        # save the model
        self.model.save(self.modelName)
        print("Model is saved")
        
        self.__summary()
    # endregion

    ########################################################################
    # private methods
    ########################################################################
    # region
    def __setDataTrain(self):
        self.train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.directory,
            validation_split=0.2,
            subset="training",
            color_mode="grayscale",
            image_size=(self.imgHeight, self.imgWidth),
            seed=123,
            batch_size=self.batch_size)

    def __setDataVal(self):
        self.val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            self.directory,
            validation_split=0.2,
            subset="validation",
            color_mode="grayscale",
            image_size=(self.imgHeight, self.imgWidth),
            seed=123,
            batch_size=self.batch_size)

    def __classCheck(self):
        print("classes expected: " +
              str(Classification.classStr(self.classification)))
        print("encountered classes " + 
              str(self.train_ds.class_names))
        if set(Classification.classStr(self.classification)) != set(self.train_ds.class_names):
            raise Exception("classes are not equal")

    def __summary(self):
        # evaluation data of the trained model
        acc = self.history.history['accuracy']
        val_acc = self.history.history['val_accuracy']
        loss = self.history.history['loss']
        val_loss = self.history.history['val_loss']
        epochs_range = range(self.epochs)
        # save data into the model folder
        np.savetxt(self.modelName + "/TrainResultsAcc.txt",
                   np.column_stack((epochs_range, acc, val_acc))[:, :],
                   fmt="%s")
        np.savetxt(self.modelName + "/TrainResultsLoss.txt",
                   np.column_stack((epochs_range, loss, val_loss))[:, :],
                   fmt="%s")
        # save the model summary and the amount of data used to
        # create the model
        with open((self.modelName + "/TrainResultsModel.txt"), 'w') as f:
            with redirect_stdout(f):
                print("amount of files used")
                print("validation split is set to 0.2\n")
                for i in (Classification.classStr(self.classification)):
                    DIR = self.directory + str(i)
                    amount = str(len([name for name in os.listdir(DIR) if
                                      os.path.isfile(os.path.join(DIR, name))
                                      ]))
                    print("class " + str(i))
                    print("amount " + amount)
                print("\nmodel summary\n")
                self.model.summary()
    # endregion

############################################################################
# child class used for using for loading a model and performing predictions
# with the loaded model.
#
# Two different public methods are available, where one performs
# a prediction based on a single image (imageSingle). The other method
# performs the model on the complete given directory.
############################################################################


class Load(CNN):
    ########################################################################
    # class constructor
    ########################################################################
    # region
    def __init__(self, modelName, directory, outDirectory, threads, 
                hardware, classification):
        CNN.__init__(self, modelName, directory, threads, hardware, classification)
        self.loadedModel = keras.models.load_model(self.modelName)
        self.outDirectory = outDirectory
        self.resultsData = np.empty((0, 6), float)
    # endregion

    ########################################################################
    # public methods
    ########################################################################
    # region
    def imageSingle(self, imageName):
        self.resultsData = np.empty((0, 6), float)
        self.__performPrediction(self.directory + imageName)

    def imageFolder(self):
        totalAmountOfImages = str(len(os.listdir(self.directory)) - 1)
        print("total amount of Images " + totalAmountOfImages)
        self.resultsData = np.empty((0, 6), float)
        with os.scandir(self.directory) as i:
            for image in i:
                if image.is_file():
                    self.__performPrediction(image.name)
        return totalAmountOfImages

    def generateReport(self):
        maxOfImages = int(max(self.resultsData[:, 0])) + 1
        minOfImages = int(min(self.resultsData[:, 0]))
        # sort on image value number
        self.resultsData = self.resultsData[self.resultsData[:, 0].
                                            argsort()]
        # i is the global counter which counts through all positions
        i = 0
        for x in range(minOfImages, maxOfImages):
            temp = np.empty((0, 5), float)
            while int(self.resultsData[i][0]) == x:
                temp = np.append(temp,
                                 np.array([[self.resultsData[i][1],
                                            self.resultsData[i][2],
                                            self.resultsData[i][3],
                                            self.resultsData[i][4],
                                            self.resultsData[i][5],
                                            ]]), axis=0)
                i += 1
                if i >= len(self.resultsData):
                    break
            # sort on middle snp
            temp = temp[temp[:, 2].argsort()]
            # save the log file
            np.savetxt(self.outDirectory + str(x) + ".txt",
                       temp[:][:], fmt="%s")
    # endregion

    ########################################################################
    # private methods
    ########################################################################
    # region
    def __performPrediction(self, imageName):
        img = tf.keras.preprocessing.image.load_img(
            self.directory + imageName,
            color_mode="grayscale",
            target_size=None
        )
        # create an image array from the image
        img_array = keras.preprocessing.image.img_to_array(img)
        # perform the pre-processing
        img_array = (img_array * (1./255))
        # add the dimension
        img_array = tf.expand_dims(img_array, 0)
        
        with tf.device(self.useDevice):
            predictions = self.loadedModel.predict(img_array)
        score = predictions[0]

        startPos = imageName.rfind(".n_")
        midPos1 = imageName.rfind(".w_start_")
        midPos2 = imageName.rfind(".w_end_")
        endPos = imageName.rfind(".png")
        firstSNP = float(imageName[midPos1 + len(".w_start_"):midPos2])
        lastSNP = float(imageName[midPos2 + len(".w_end_"):endPos])
        middleSNP = (firstSNP + lastSNP) / 2
        # print(Classification.classStr(self.classification))
        # write output when using 
        if (len(Classification.classStr(self.classification)) == 2):
            scoreNeutral = score[0]
            scoreSelected = score[1]
            self.resultsData = np.append(self.resultsData,
                                        np.array([[float(imageName
                                                        [startPos +
                                                        len(".n_"):
                                                        midPos1]),
                                                    firstSNP, lastSNP,
                                                    middleSNP,
                                                    float(scoreNeutral),
                                                    float(scoreSelected)]]),
                                        axis=0)
        
        if (len(Classification.classStr(self.classification)) == 3):
            scoreNeutral = score[0]
            scoreHard = score[1]
            scoreSoft = score[2]
            self.resultsData = np.append(self.resultsData,
                                        np.array([[float(imageName
                                                        [startPos +
                                                        len(".n_"):
                                                        midPos1]),
                                                    firstSNP, lastSNP,
                                                    middleSNP,
                                                    float(scoreNeutral),
                                                    float(scoreHard),
                                                    float(scoreSoft)]]),
                                        axis=0)
    # endregion
