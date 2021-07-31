#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script for the delete of a new folder"
    echo ""
    echo "$0"
    echo "-d Directory to delete"
    echo -e "\t-d Directory to delete"
    exit 1
}

while getopts "hd:" flag
do
    case "${flag}" in
        d) directory=${OPTARG} ;;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$directory" ]
then 
    echo "Some or all of the parameters are empty";
    helpFunction
fi

echo "deleting the complete $directory folder";
rm -r -f $directory/