#!/usr/bin/python
############################################################################
# File:			datatypes.py
# Organization:	University of twente
# Group:		CAES
# Date:			15-10-2021
# Version:		2.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Some new datatypes used on various places in ASDEC
############################################################################

from enum import Enum

# region define new types
class Hardware(Enum):
    NULL = 0
    CPU = 1
    GPU = 2
    
    @staticmethod
    def fromStr(label):
        if (label == Hardware.NULL):
            return "NULL"
        elif (label == Hardware.CPU):
            return "CPU"
        elif (label == Hardware.GPU):
            return "GPU"
        else:
            raise NotImplementedError

class Classification(Enum):
    NULL = 0
    NS = 1
    NH = 2
    NHS = 3

    @staticmethod
    def fromStr(label):
        if (label == Classification.NULL):
            return "NULL"
        elif (label == Classification.NS):
            return ["neutral" , "soft"]
        elif (label == Classification.NH):
            return ["neutral", "hard"]
        elif (label == Classification.NHS):
            return ["neutral", "hard", "soft"]
        else:
            raise NotImplementedError
# endregion
