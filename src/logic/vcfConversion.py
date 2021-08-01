#!/usr/bin/python
############################################################################
# File:			vcfConversion.py
# Organization:	University of twente
# Group:		CAES
# Date:			31-07-2021
# Version:		1.0.0
# Author:		Matthijs Souilljee, s2211246
# Education:	EMSYS msc.
############################################################################
# converts of a vcf file
############################################################################
import shlex
import subprocess

def vcfConversion(inputfile, chromosomeLength, memorySize):
    if inputfile.endswith(".vcf"):
        subprocess.call(shlex.split('./RAiSD_Parser/RAiSD' +
                                    ' -n ' + 'test_run' +
                                    ' -I ' + str(inputfile) +
                                    ' -L ' + str(chromosomeLength) +
                                    ' -Q ' + str(memorySize) + 
                                    ' -f '))
        inputfile = inputfile + ".ms"
        # delete the logfiles of RAiSD
        subprocess.call(shlex.split('rm RAiSD_Info.test_run'))
        subprocess.call(shlex.split('rm RAiSD_Report.test_run'))
        return True
    return False
