############################################################################
# File:			originalModel.py
# Organization:	University of twente
# Group:		CAES
# Date:			26-03-2021
# Version:		0.0.1
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Really simpel model based on the example from the tensorflow website
# src: https://www.tensorflow.org/tutorials/images/classification
# Use this model as a template when designing your own
############################################################################

# region import packages
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import (layers, models, activations,
                              optimizers, regularizers)
# endregion

def model(amountOfClasses, shapeIn):
    ####################################################################
    # Defining the model
    ####################################################################
    model = tf.keras.Sequential([
        layers.Conv2D(2, 3, padding='same', input_shape=shapeIn[1:], activation='relu'),
        layers.MaxPooling2D(pool_size=(
            2, 2), strides=(1, 1), padding='valid'),
        layers.Conv2D(2, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(pool_size=(
            2, 2), strides=(1, 1), padding='valid'),
        layers.Conv2D(2, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(pool_size=(
            2, 2), strides=(1, 1), padding='valid'),
        layers.Conv2D(2, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(pool_size=(
            2, 2), strides=(1, 1), padding='valid'),
        layers.Conv2D(2, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(pool_size=(
            2, 2), strides=(1, 1), padding='valid'),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        # Do not use a softmax layer here, because
        # it will break the loading
        layers.Dense(amountOfClasses, activation='softmax')
    ])
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