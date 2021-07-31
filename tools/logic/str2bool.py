#!/usr/bin/python
############################################################################
# File:			str2bool.py
# Organization:	University of twente
# Group:		CAES
# Date:			10-03-2021
# Version:		0.0.1
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# converts a string to a boolean
############################################################################


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
