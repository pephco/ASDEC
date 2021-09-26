############################################################################
# File:			ModelDesignA.py
# Organization:	University of twente
# Group:		CAES
# Date:			21-04-2021
# Version:		0.0.1
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Model design based on some ideas
############################################################################

# region import packages
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import (utils, layers, models, activations,
                              optimizers, regularizers, Model)
from keras.layers.normalization import BatchNormalization
# endregion

def model(amountOfClasses, shapeIn):
    ksize = (10,10)
    stride = (1,1)
    l2_lambda = 0.0001
    pool = (2,2)
    ####################################################################    
    # Defining the model
    ####################################################################
    inputs = layers.Input(shape=shapeIn[1:])
    
    sweepcnn = layers.Conv2D(filters=32, kernel_size=ksize, padding='same', strides=stride, 
        activation='relu') (inputs)
    # sweepcnn = layers.BatchNormalization()(sweepcnn)
    sweepcnn = layers.MaxPooling2D(pool_size=pool, strides=stride, padding='same')(sweepcnn)
    
    sweepcnn = layers.Conv2D(filters=32, kernel_size=ksize, padding='same', strides=stride, 
        activation='relu') (sweepcnn)
    # sweepcnn = layers.BatchNormalization()(sweepcnn)
    sweepcnn = layers.MaxPooling2D(pool_size=pool, strides=stride, padding='same')(sweepcnn)
    
    sweepcnn = layers.Conv2D(filters=32, kernel_size=ksize, padding='same', strides=stride, 
        activation='relu') (sweepcnn)
    # sweepcnn = layers.BatchNormalization()(sweepcnn)
    sweepcnn = layers.MaxPooling2D(pool_size=pool, strides=stride, padding='same')(sweepcnn)
    
    # flatten to a 1d tensor
    sweepcnn = layers.Flatten()(sweepcnn)
    
    sweepcnn = layers.Dense(512, activation='relu')(sweepcnn)
    # sweepcnn = layers.BatchNormalization()(sweepcnn)
    prediction = layers.Dense(amountOfClasses, activation='softmax')(sweepcnn)
    
    model = models.Model(inputs=inputs, outputs=prediction)
    ####################################################################

    
    ####################################################################
    # Compile
    ####################################################################
    model.compile(
            optimizer='adam',
            loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
    ####################################################################
    
    return model