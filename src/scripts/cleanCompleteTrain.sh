#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script which creates a folder including structure for training a model" 
    echo "inside of a given path. Included with the pad should be"
    echo "the desired name of the folder. For example '-d out/testfolder/'"
    echo "now the folder out should already. exists and the testfolder"
    echo "will be created with the corresponding content."
    echo ""
    echo "$0"
    echo "-d Directory to start creation"
    echo -e "\t-d Directory path where to create the file structure"
    echo -e "\t-i Class name to create folders for"
    exit 1
}

while getopts "hd:i:" flag
do
    case "${flag}" in
        d) directory=${OPTARG};;
        i) className=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$directory" ] || [ -z "$className" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

echo "creating new file structure";
mkdir -p $directory/
mkdir -p $directory/img
mkdir -p $directory/img/$className
mkdir -p $directory/raw
mkdir -p $directory/raw/$className
echo "Done";