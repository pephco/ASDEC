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
from keras.utils.vis_utils import plot_model
# endregion

def model(amountOfClasses, shapeIn):
    ksize = (2,2)
    stride = (1,1)
    l2_lambda = 0.0001
    pool = (2,2)
    ####################################################################    
    # Defining the model
    ####################################################################
    model = models.Sequential([
                    layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), padding='valid', input_shape=gene_sim.data.shape[1:]),
                    layers.MaxPooling2D(pool_size=(2,2)),
                    layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), padding='valid'),
                    layers.MaxPooling2D(pool_size=(2,2)),
                    layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), padding='valid'),
                    layers.MaxPooling2D(pool_size=(2,2)),
                    layers.Flatten(),
                    layers.Dense(units=128, activation='relu'),
                    layers.Dense(units=len(gene_sim.classes), activation='softmax')])
    ####################################################################

    
    ####################################################################
    # Compile 
    ####################################################################

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    
    return model