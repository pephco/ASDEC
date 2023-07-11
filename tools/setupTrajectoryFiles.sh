#!/bin/bash
# author: Matthijs Souilljee, University of Twente
# Get the trajectory files from a public google drive
mkdir -p trajectory_files/
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=19zpUZEp2TAzpuFHiE-YYK1GW4lOdJdsp' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=19zpUZEp2TAzpuFHiE-YYK1GW4lOdJdsp" -O trajectory_files.zip && rm -rf /tmp/cookies.txt
unzip trajectory_files.zip && rm trajectory_files.zip
