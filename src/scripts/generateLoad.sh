#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script for running a single thread."
    echo "Normally this script is not run itself but called by"
    echo "pipelineLoad.sh. If it is desired to be called some"
    echo "enforce the standard folder and file structure,"
    echo "also ensure that all inputs are possible"
    echo ""
    echo "$0"
    echo "-a thread number -b start population -c end population"
    echo "-d MS/MSSel file -e imageName -f window bool trigger"
    echo "-g window length -i step size window -j center bool trigger"
    echo "-k center range -l multiplication -m model + path"
    echo "-n window height/individuals -o added name field"
    echo "-p folder structure root folder -q directory save post log files"
    echo "-r mode post -s param a post -t param b post"
    echo "-u directory save summary files -v steps per thread"
	echo "-x directory save pre post log files"
	echo "-y extraction point in position"
	echo "-z memory reguirement vcf parser"
	echo "-Z chromosome length reguirement vcf parser"
	echo "-X device: --GPU or --CPU"
    echo "-Y Classification: --NH, --NS, or --NHS"
    echo ""

}

while getopts "ha:b:c:d:e:f:g:i:j:k:l:m:n:o:p:q:r:s:t:u:v:x:y:z:Z:X:Y:" flag
do
    case "${flag}" in
        a) thread=${OPTARG};;
        b) start=${OPTARG};;
        c) end=${OPTARG};;
        d) inMsMssel=${OPTARG};;
        e) imageName=${OPTARG};;
        f) windowEnb=${OPTARG};;
        g) windowSize=${OPTARG};;
        i) stepSize=${OPTARG};;
        j) centerEnb=${OPTARG};;
        k) centerOff=${OPTARG};;
        l) multiplication=${OPTARG};;
        m) model=${OPTARG};;
        n) imageHeight=${OPTARG};;
        o) outlog=${OPTARG};;
        p) folderName=${OPTARG};;
        q) savePost=${OPTARG};;
        r) postMode=${OPTARG};;
        s) parama=${OPTARG};;
        t) paramb=${OPTARG};;
        u) saveSummary=${OPTARG};;
        v) stepsPerThread=${OPTARG};;
		x) logPrePost=${OPTARG};;
		y) extractionPoint=${OPTARG};;
		z) memorySize=${OPTARG};;
		Z) chromosomeLength=${OPTARG};;
		X) inputLineHardware=${OPTARG};;
        Y) inputLineTraining=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$thread" ] || [ -z "$start" ] || [ -z "$end" ] || [ -z "$inMsMssel" ] || [ -z "$imageName" ] || [ -z "$windowEnb" ] || [ -z "$windowSize" ] || [ -z "$stepSize" ] || [ -z "$centerEnb" ] || [ -z "$centerOff" ] || [ -z "$multiplication" ] || [ -z "$model" ] || [ -z "$imageHeight" ] || [ -z "$outlog" ] || [ -z "$folderName" ] || [ -z "$savePost" ] || [ -z "$postMode" ] || [ -z "$parama" ] || [ -z "$paramb" ] || [ -z "$saveSummary" ] || [ -z "$stepsPerThread" ] || [ -z "$logPrePost" ] || [ -z "$extractionPoint" ] || [ -z "$memorySize" ] || [ -z "$chromosomeLength" ] || [ -z "$inputLineTraining" ] || [ -z "$inputLineHardware" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

for number in `seq $(($start-1)) $stepsPerThread $(($end-1))`
do
    if [ "$(($number+$stepsPerThread))" -gt "$(($end))" ]
    then
        echo "Adjusted steps per thread to $(($end-$start+1))"
        jump=$(($end))
    else
        jump=$(($number+$stepsPerThread))
    fi
    echo "itteration number: $number"
    rsync -a --delete $folderName/blank/ $folderName/unknown$thread/
    python3 src/callerBitmap.py -i $inMsMssel -o $folderName/unknown$thread/$imageName -w $windowEnb -s $stepSize -l $windowSize -c $centerEnb -z $centerOff -m $multiplication -a $number -e $jump -v "${saveSummary}/info/threadTime_$thread.txt" -p $extractionPoint -x $memorySize -X $chromosomeLength
    
    rsync -a --delete $folderName/blank/ $folderName/log$thread/
    python3 src/callerLoadCNN.py -m $model -d $folderName/unknown$thread/ -o $folderName/log$thread/logTraj$outlog -v "${saveSummary}/info/threadTime_$thread.txt" "${inputLineTraining}" "${inputLineHardware}" -t 1
    
    if [ "${saveSummary}" != "NULL" ]
    then
        rsync -a --delete $folderName/blank/ $folderName/sum$thread/
        python3 src/callerPostProcessing.py -i $folderName/log$thread/ -o $savePost -s $folderName/sum$thread/ -m $postMode -a $parama -b $paramb -v "${saveSummary}/info/threadTime_$thread.txt" -x $logPrePost
        cat $folderName/sum$thread/*.txt >> $folderName/sum/$thread.txt 
    else
        python3 src/callerPostProcessing.py -i $folderName/log$thread/ -o $savePost -s NULL -m $postMode -a $parama -b $paramb -x $logPrePost
    fi
done