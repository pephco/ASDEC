#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script for the creation of a new folder"
    echo ""
    echo "$0"
    echo "-d Directory to create"
    echo -e "\t-d Directory to create"
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

echo "making the complete $directory folder";
mkdir -p $directory