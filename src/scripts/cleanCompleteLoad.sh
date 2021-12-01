#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script which creates a folder including structure for using/loading a model" 
    echo "inside of a given path. Included with the pad should be"
    echo "the desired name of the folder. For example '-d out/testfolder/'"
    echo "now the folder out should already. exists and the testfolder"
    echo "will be created with the corresponding content."
    echo ""
    echo "$0"
    echo "-t Amount of threads -d Directory to start creation"
    echo -e "\t-t Amount of threads that folders need to be created for"
    echo -e "\t-d Directory path where to create the file structure"
    echo -e "\t-f Folders inside the directory"
    exit 1
}

while getopts "ht:d:f:" flag
do
    case "${flag}" in 
        t) threads=${OPTARG};;
        d) directory=${OPTARG};;
        f) folders=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$threads" ] || [ -z "$directory" ] || [ -z "$folders" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

echo "amount of threads: $threads";
echo "creating new file structure";
mkdir -p $directory/
mkdir -p $directory/blank
mkdir -p $directory/raw
for folder in ${folders[@]}; do
    mkdir -p $directory/raw/$folder
done 
mkdir -p $directory/sum
for number in `seq 1 $threads`; do \
    mkdir -p $directory/unknown$number ; \
    mkdir -p $directory/log$number ; \
    mkdir -p $directory/sum$number ; \
done
echo "Done";