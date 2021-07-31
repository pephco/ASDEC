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
    exit 1
}

while getopts "hd:" flag
do
    case "${flag}" in
        d) directory=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$directory" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

echo "creating new file structure";
mkdir $directory/
mkdir $directory/img
mkdir $directory/img/neutral
mkdir $directory/img/selection
mkdir $directory/raw
mkdir $directory/raw/neutral
mkdir $directory/raw/selection 
echo "Done";