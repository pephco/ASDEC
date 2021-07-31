#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script to create a file structure and start files for the timing"
    echo ""
    echo "$0"
    echo "-t Amount of threads -d Directory to start creation"
    echo -e "\t-t Amount of threads that folders need to be created for"
    echo -e "\t-d Directory path where to create the file structure"
    exit 1
}

while getopts "ht:d:" flag
do
    case "${flag}" in 
        t) threads=${OPTARG};;
        d) directory=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$threads" ] || [ -z "$directory" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

echo "creating file structure ";
mkdir -p "${directory}info"
mkdir -p "${directory}results"
mkdir -p "${directory}preLog"
mkdir -p "${directory}postLog"
for number in `seq 1 $threads`
do 
    echo "Time summary in seconds of thread ${number}" > $directory/info/threadTime_$number.txt
done