#!/usr/bin/python
############################################################################
# File:			randomGenerator.py
# Organization:	University of twente
# Group:		CAES
# Date:			31-07-2021
# Version:		1.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# Has a function which generates a random sequence of numbers and
# letters.
# source: https://stackoverflow.com/questions/2257441/
#   random-string-generation-with-upper-case-letters-and-digits
############################################################################


# region import packages
import string
import random
# endregion

# region methods


def id_generator(size=12, chars=string.ascii_uppercase
                 + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
# endregion
