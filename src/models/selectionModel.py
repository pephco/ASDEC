############################################################################
# File:			selectionModel.py
# Organization:	University of twente
# Group:		CAES
# Date:			09-04-2021
# Version:		0.0.1
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Model based on the paper: The Unreasonable Effectiveness of Convolutional 
# Neural Networks in Population Genetic Inference by Lex Flagel, 
# Yaniv Brandvain, and Daniel Schrider. https://doi.org/10.1101/336073
# 
# Github page: https://github.com/flag0010/pop_gen_cnn
#
# Model was changed in a couple of ways to make it work with the dataset
#   - Merge layer (deprecated by tensorflow) replaced by concat layer 
#   - Different writing style
#   - Pre-processing step to bring all value between 0 and 1
#   - 
############################################################################

# region import packages
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import (layers, models, activations,
                              optimizers, regularizers, Model)
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, concatenate, Concatenate, Input, Add, Reshape
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Conv1D, MaxPooling1D, AveragePooling1D
# endregion

def model(amountOfClasses, shapeIn, callbacks, train_ds, val_ds, epochs):
    # create a kernel with a height of 1
    # the result will be similair to that
    # of a 1D convolutional
    ksize = 2
    l2_lambda = 0.0001
    # val_ds = sequence.pad_sequences(val_ds, padding='post',  maxlen=5000)
    # train_ds = sequence.pad_sequences(train_ds, padding='post',  maxlen=5000)
    ####################################################################
    # Defining the model
    ####################################################################
    model1 = Sequential(layers=[
        Reshape((shapeIn[1]*shapeIn[2],shapeIn[3]), input_shape=shapeIn[1:]),
        layers.experimental.preprocessing.Rescaling(1./255),
        Conv1D(128*2, kernel_size=ksize, activation='relu',kernel_regularizer=keras.regularizers.l2(l2_lambda)),
        Conv1D(128*2, kernel_size=ksize, activation='relu',kernel_regularizer=keras.regularizers.l2(l2_lambda)),
        MaxPooling1D(pool_size=(ksize)),
        Dropout(0.2),
        
        Conv1D(128*2, kernel_size=ksize, activation='relu',kernel_regularizer=keras.regularizers.l2(l2_lambda)),
        MaxPooling1D(pool_size=(ksize)),
        Dropout(0.2),
        
        Conv1D(128*2, kernel_size=ksize, activation='relu',kernel_regularizer=keras.regularizers.l2(l2_lambda)),
        AveragePooling1D(pool_size=(ksize)),
        Dropout(0.2),
        
        Conv1D(128*2, kernel_size=ksize,activation='relu',kernel_regularizer=keras.regularizers.l2(l2_lambda)),
        AveragePooling1D(pool_size=(ksize)),
        Dropout(0.2),
        
        Flatten(),
        Dense(amountOfClasses),
    ])
    
    # still need to define a corresponding input for this one
    model2 = Sequential(layers=[
        layers.experimental.preprocessing.Rescaling(1./255),
        Dense(64, activation='relu',kernel_regularizer=keras.regularizers.l2(l2_lambda)),
        Dropout(0.1),
        Flatten(),
    ])
    
    # for a common input
    commonInput = Input(shape=shapeIn[1:])
    out1 = model1(commonInput)    
    out2 = model2(commonInput)    
    
    # for two inputs
    # input1 = Input(shape=(shapeIn[1], shapeIn[2], 3))
    # input2 = Input(shape=(shapeIn[1], shapeIn[2], 3))
    # out1 = model1(input1)
    # out2 = model2(input2)
    
    mergedOut = Concatenate()([out1,out2])
    mergedOut = Dense(256, activation='relu', kernel_initializer='normal',kernel_regularizer=keras.regularizers.l2(l2_lambda))(mergedOut)
    mergedOut = Dropout(0.25)(mergedOut)        
    mergedOut = layers.Dense(amountOfClasses)(mergedOut)

    # output layer
    
    # for common input
    oneInputModel = Model(commonInput,mergedOut)
    
    
    # for different inputs use
    # twoInputModel = Model([input1,input2], mergedOut)
    # return twoInputModel
    ####################################################################
    
    ####################################################################
    # Compile and fit
    ####################################################################
    model = model1
    model.compile(
            optimizer='adam',
            loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
    # model.compile(loss=keras.losses.categorical_crossentropy,
              # optimizer=keras.optimizers.Adam(),
              # metrics=['accuracy'])
              
    history = model.fit(
            train_ds,
            validation_data=val_ds,
            verbose=1,
            epochs=epochs,
            callbacks=callbacks
            )
    # self.history = self.model.fit(
            # [self.train_ds, self.train_ds],
            # validation_data=[self.val_ds,self.val_ds],
            # verbose=1,
            # epochs=self.epochs,
            # callbacks=[model_checkpoint_callback, tensorboard_callback]
        # )
    ####################################################################
    
    ####################################################################
    # Callback
    # only if you are using callback[0]
    ####################################################################
    # The model weights (that are considered the best) are loaded into the model.
    self.model.load_weights(self.modelName + "/checkpoint")
    ####################################################################
    
    return model, history