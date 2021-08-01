#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "Script that will call all the threads."
    echo "The amount of threads should be considered correctly"
    echo "so that division by zero and decimal numbers are avoided"
    echo "ensure that number population (n) % threads (a) == 0."
    echo "Also threads should never equal 0!"
    echo "This scripts does not provide any protection against wrong inputs"
    echo "Again the standard project folder and file structure should be enforced"
    echo ""
    echo "$0"
    echo "-a amount of threads -b MS/MSSel file -c imageName -d window bool trigger"
    echo "-e window length -f step size window -g center bool trigger"
    echo "-i center range -j multiplication -k model + path -l window height/individuals"
    echo "-m added name field -n number of populations -o folder structure root folder"
    echo "-p directory save post log files -q mode post -r param a post -s param b post"
    echo "-t directory save summary files + info -u steps per thread"
	echo "-x directory save pre post log files"
	echo "-y extraction position"
	echo "-z memory reguirement vcf parser"
	echo "-Z chromosome length reguirement vcf parser"
    exit 1
}

while getopts "ha:b:c:d:e:f:g:i:j:k:l:m:n:o:p:q:r:s:t:u:x:y:z:Z:" flag
do
    case "${flag}" in
        a) thread=${OPTARG};;
        b) inMsMssel=${OPTARG};;
        c) imageName=${OPTARG};;
        d) windowEnb=${OPTARG};;
        e) windowSize=${OPTARG};;
        f) stepSize=${OPTARG};;
        g) centerEnb=${OPTARG};;
        i) centerOff=${OPTARG};;
        j) multiplication=${OPTARG};;
        k) model=${OPTARG};;
        l) windowHeight=${OPTARG};;
        m) outlog=${OPTARG};;
        n) numberOfPopulations=${OPTARG};;
        o) folderName=${OPTARG};;
        p) savePost=${OPTARG};;
        q) postMode=${OPTARG};;
        r) parama=${OPTARG};;
        s) paramb=${OPTARG};;
        t) saveSummary=${OPTARG};;
        u) stepsPerThread=${OPTARG};;
		x) logPrePost=${OPTARG};;
		y) extractionPoint=${OPTARG};;
		z) memorySize=${OPTARG};;
		Z) chromosomeLength=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done

if [ -z "$thread" ] || [ -z "$inMsMssel" ] || [ -z "$imageName" ] || [ -z "$windowEnb" ] || [ -z "$windowSize" ] || [ -z "$stepSize" ] || [ -z "$centerEnb" ] || [ -z "$centerOff" ] || [ -z "$multiplication" ] || [ -z "$model" ] || [ -z "$windowHeight" ] || [ -z "$outlog" ] || [ -z "$numberOfPopulations" ] || [ -z "$folderName" ] || [ -z "$savePost" ] || [ -z "$postMode" ] || [ -z "$parama" ] || [ -z "$paramb" ] || [ -z "$saveSummary" ] || [ -z "$stepsPerThread" ] || [ -z "$logPrePost" ] || [ -z "$extractionPoint" ] || [ -z "$memorySize" ] || [ -z "$chromosomeLength" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

rsync -a --delete $folderName/blank/ $folderName/sum/

for number in `seq 1 $thread`
do
    echo "start thread number: $number"
    echo "start population: $((($number - 1) * ($numberOfPopulations / $thread) + 1))"
    echo "end population: $((($number) * ($numberOfPopulations / $thread)))"
    ./src/scripts/generateLoad.sh -a $number \
    -b $((($number - 1) * ($numberOfPopulations / $thread) + 1)) \
    -c $((($number) * ($numberOfPopulations / $thread))) \
    -d $inMsMssel \
    -e $imageName \
    -f $windowEnb \
    -g $windowSize \
    -i $stepSize \
    -j $centerEnb \
    -k $centerOff \
    -l $multiplication \
    -m $model \
    -n $windowHeight \
    -o $outlog \
    -p $folderName \
    -q $savePost \
    -r $postMode \
    -s $parama \
    -t $paramb \
    -u $saveSummary \
    -v $stepsPerThread \
	-x $logPrePost \
	-y $extractionPoint \
	-z $memorySize \
	-Z $chromosomeLength&
done
wait

if [ "${saveSummary}" != "NULL" ]
then
    echo "create final summary"
    echo -n > "${saveSummary}logTraj${outlog}summary.txt"
    for number in `seq 1 $thread`
    do
        cat $folderName/sum/$number.txt >> "${saveSummary}logTraj${outlog}summary.txt"
    done
fi