#!/bin/bash
# author: Matthijs Souilljee, University of Twente
helpFunction()
{
    echo ""
    echo "generate both the data considering the natural and the selected mutations"
    echo ""
    echo "$0"
    echo "-s start BASE -e end BASE -b start TEST -f end TEST -i number of populations"
    echo "-c number of individuals -d output directory (should be in format)"
    echo -e "\t-s start number of simulation of BASE"
    echo -e "\t-e end number of simulations of BASE"
    echo -e "\t-b start number of simulation of TEST"
    echo -e "\t-f end number of simulations of TEST"
    echo -e "\t-i number of populations per file/simulation"
    echo -e "\t-c number of individuals per population"
    echo -e "\t-d output directory to write to (!SHOULD BE IN CORRECT FORMAT! SEE DOCUMENTATION)"
	echo -e "\t-t number of threads used"
    exit 1
}

while getopts "hs:e:b:f:i:c:d:t:" flag
do
    case "${flag}" in
        s) startBASEIn=${OPTARG};;
        e) endBASEIn=${OPTARG};;
        b) startTESTIn=${OPTARG};;
        f) endTESTIn=${OPTARG};;
        i) numberOfPopulations=${OPTARG};;
        c) individuals=${OPTARG};;
        d) directory=${OPTARG};;
		t) threads=${OPTARG};;
        h) helpFunction ;;
        ?) helpFunction ;;
    esac
done
if [ -z "$startBASEIn" ] || [ -z "$endBASEIn" ] || [ -z "$startTESTIn" ] || [ -z "$endTESTIn" ] || [ -z "$numberOfPopulations" ] || [ -z "$individuals" ] || [ -z "$directory" ] || [ -z "$threads" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

echo "startBASE BASE: $startBASEIn";
echo "endBASE BASE: $endBASEIn";
echo "startBASE TEST: $startTESTIn";
echo "endBASE TEST: $endTESTIn";
echo "with number of populations: $numberOfPopulations"
echo "individuals per population: $individuals"
echo "saving to directory: $directory"

for i in `seq 0 $threads $((endBASEIn-startBASEIn))`
do
	startBASE=$((startBASEIn+i))
	endBASE=$((startBASEIn+threads+i-1))
	if [[ $endBASE -gt $endBASEIn ]]
	then
		endBASE=$((endBASEIn))
	fi
	##################
	## BASE files ####
	##################
	if [[ $startBASE -gt 0 ]]
	then
		echo starting BASE Threads
		echo "start ${startBASE}"
		echo "end ${endBASE}"
	fi
	################################################################################################################################################################
	if [[ $startBASE -le 1 && $endBASE -ge 1 ]]
	then
		echo "run BASE 1";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE1.txt &
	fi
	if [[ $startBASE -le 2 && $endBASE -ge 2 ]]
	then
		echo "run BASE 2";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10100000000000000000 1 > $directory/raw/neutral/BASE2.txt &
	fi
	if [[ $startBASE -le 3 && $endBASE -ge 3 ]]
	then
		echo "run BASE 3";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10200000000000000000 1 > $directory/raw/neutral/BASE3.txt &
	fi
	if [[ $startBASE -le 4 && $endBASE -ge 4 ]]
	then
		echo "run BASE 4";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.1 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE4.txt &
	fi
	if [[ $startBASE -le 5 && $endBASE -ge 5 ]]
	then
		echo "run BASE 5";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.1 -eN .10100000000000000000 1 > $directory/raw/neutral/BASE5.txt &
	fi
	if [[ $startBASE -le 6 && $endBASE -ge 6 ]]
	then
		echo "run BASE 6";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.1 -eN .10200000000000000000 1 > $directory/raw/neutral/BASE6.txt &
	fi

	if [[ $startBASE -le 7 && $endBASE -ge 7 ]]
	then
		echo "run BASE 7";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.01 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE7.txt &
	fi
	if [[ $startBASE -le 8 && $endBASE -ge 8 ]]
	then
		echo "run BASE 8";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.01 -eN .10100000000000000000 1 > $directory/raw/neutral/BASE8.txt &
	fi
	if [[ $startBASE -le 9 && $endBASE -ge 9 ]]
	then
		echo "run BASE 9";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.01 -eN .10200000000000000000 1 > $directory/raw/neutral/BASE9.txt &
	fi
	if [[ $startBASE -le 10 && $endBASE -ge 10 ]]
	then
		echo "run BASE 10";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.005 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE10.txt &
	fi
	if [[ $startBASE -le 11 && $endBASE -ge 11 ]]
	then
		echo "run BASE 11";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.005 -eN .10100000000000000000 1 > $directory/raw/neutral/BASE11.txt &
	fi
	if [[ $startBASE -le 12 && $endBASE -ge 12 ]]
	then
		echo "run BASE 12";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.005 -eN .10200000000000000000 1 > $directory/raw/neutral/BASE12.txt &
	fi

	if [[ $startBASE -le 13 && $endBASE -ge 13 ]]
	then
		echo "run BASE 13";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.5 -eN .02040000000000000000 1 > $directory/raw/neutral/BASE13.txt &
	fi
	if [[ $startBASE -le 14 && $endBASE -ge 14 ]]
	then
		echo "run BASE 14";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.5 -eN .02100000000000000000 1 > $directory/raw/neutral/BASE14.txt &
	fi
	if [[ $startBASE -le 15 && $endBASE -ge 15 ]]
	then
		echo "run BASE 15"
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.5 -eN .02200000000000000000 1 > $directory/raw/neutral/BASE15.txt &
	fi
	if [[ $startBASE -le 16 && $endBASE -ge 16 ]]
	then
		echo "run BASE 16";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.1 -eN .02040000000000000000 1 > $directory/raw/neutral/BASE16.txt &
	fi
	if [[ $startBASE -le 17 && $endBASE -ge 17 ]]
	then
		echo "run BASE 17";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.1 -eN .02100000000000000000 1 > $directory/raw/neutral/BASE17.txt &
	fi
	if [[ $startBASE -le 18 && $endBASE -ge 18 ]]
	then 
		echo "run BASE 18";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.1 -eN .02200000000000000000 1 > $directory/raw/neutral/BASE18.txt &
	fi

	if [[ $startBASE -le 19 && $endBASE -ge 19 ]]
	then
		echo "run BASE 19";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.01 -eN .02040000000000000000 1 > $directory/raw/neutral/BASE19.txt &
	fi
	if [[ $startBASE -le 20 && $endBASE -ge 20 ]]
	then
		echo "run BASE 20";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.01 -eN .02100000000000000000 1 > $directory/raw/neutral/BASE20.txt &
	fi
	if [[ $startBASE -le 21 && $endBASE -ge 21 ]]
	then
		echo "run BASE 21";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.01 -eN .02200000000000000000 1 > $directory/raw/neutral/BASE21.txt &
	fi
	if [[ $startBASE -le 22 && $endBASE -ge 22 ]]
	then
		echo "run BASE 22";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.005 -eN .02040000000000000000 1 > $directory/raw/neutral/BASE22.txt &
	fi
	if [[ $startBASE -le 23 && $endBASE -ge 23 ]]
	then
		echo "run BASE 23";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.005 -eN .02100000000000000000 1 > $directory/raw/neutral/BASE23.txt &
	fi
	if [[ $startBASE -le 24 && $endBASE -ge 24 ]]
	then
		echo "run BASE 24";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .02000000000000000000 0.005 -eN .02200000000000000000 1 > $directory/raw/neutral/BASE24.txt &
	fi

	if [[ $startBASE -le 25 && $endBASE -ge 25 ]]
	then
		echo "run BASE 25";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.5 -eN .01540000000000000000 1 > $directory/raw/neutral/BASE25.txt &
	fi
	if [[ $startBASE -le 26 && $endBASE -ge 26 ]]
	then
		echo "run BASE 26";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.5 -eN .01600000000000000000 1 > $directory/raw/neutral/BASE26.txt &
	fi
	if [[ $startBASE -le 27 && $endBASE -ge 27 ]]
	then
		echo "run BASE 27";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.5 -eN .01700000000000000000 1 > $directory/raw/neutral/BASE27.txt &
	fi
	if [[ $startBASE -le 28 && $endBASE -ge 28 ]]
	then
		echo "run BASE 28";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.1 -eN .01540000000000000000 1 > $directory/raw/neutral/BASE28.txt &
	fi
	if [[ $startBASE -le 29 && $endBASE -ge 29 ]]
	then
		echo "run BASE 29";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.1 -eN .01600000000000000000 1 > $directory/raw/neutral/BASE29.txt &
	fi
	if [[ $startBASE -le 30 && $endBASE -ge 30 ]]
	then
		echo "run BASE 30";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.1 -eN .01700000000000000000 1 > $directory/raw/neutral/BASE30.txt &
	fi

	if [[ $startBASE -le 31 && $endBASE -ge 31 ]]
	then
		echo "run BASE 31";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.01 -eN .01540000000000000000 1 > $directory/raw/neutral/BASE31.txt &
	fi
	if [[ $startBASE -le 32 && $endBASE -ge 32 ]]
	then
		echo "run BASE 32";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.01 -eN .01600000000000000000 1 > $directory/raw/neutral/BASE32.txt &
	fi
	if [[ $startBASE -le 33 && $endBASE -ge 33 ]]
	then
		echo "run BASE 33";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.01 -eN .01700000000000000000 1 > $directory/raw/neutral/BASE33.txt &
	fi
	if [[ $startBASE -le 34 && $endBASE -ge 34 ]]
	then
		echo "run BASE 34";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.005 -eN .01540000000000000000 1 > $directory/raw/neutral/BASE34.txt &
	fi
	if [[ $startBASE -le 35 && $endBASE -ge 35 ]]
	then
		echo "run BASE 35";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.005 -eN .01600000000000000000 1 > $directory/raw/neutral/BASE35.txt &
	fi
	if [[ $startBASE -le 36 && $endBASE -ge 36 ]]
	then
		echo "run BASE 36";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01500000000000000000 0.005 -eN .01700000000000000000 1 > $directory/raw/neutral/BASE36.txt &
	fi

	if [[ $startBASE -le 37 && $endBASE -ge 37 ]]
	then
		echo "run BASE 37";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.5 -eN .01040000000000000000 1 > $directory/raw/neutral/BASE37.txt &
	fi
	if [[ $startBASE -le 38 && $endBASE -ge 38 ]]
	then
		echo "run BASE 38";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.5 -eN .01100000000000000000 1 > $directory/raw/neutral/BASE38.txt &
	fi
	if [[ $startBASE -le 39 && $endBASE -ge 39 ]]
	then
		echo "run BASE 39";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.5 -eN .01200000000000000000 1 > $directory/raw/neutral/BASE39.txt &
	fi
	if [[ $startBASE -le 40 && $endBASE -ge 40 ]]
	then
		echo "run BASE 40";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.1 -eN .01040000000000000000 1 > $directory/raw/neutral/BASE40.txt &
	fi
	if [[ $startBASE -le 41 && $endBASE -ge 41 ]]
	then
		echo "run BASE 41";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.1 -eN .01100000000000000000 1 > $directory/raw/neutral/BASE41.txt &
	fi
	if [[ $startBASE -le 42 && $endBASE -ge 42 ]]
	then
		echo "run BASE 42";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.1 -eN .01200000000000000000 1 > $directory/raw/neutral/BASE42.txt &
	fi

	if [[ $startBASE -le 43 && $endBASE -ge 43 ]]
	then
		echo "run BASE 43";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.01 -eN .01040000000000000000 1 > $directory/raw/neutral/BASE43.txt &
	fi
	if [[ $startBASE -le 44 && $endBASE -ge 44 ]]
	then
		echo "run BASE 44";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.01 -eN .01100000000000000000 1 > $directory/raw/neutral/BASE44.txt &
	fi
	if [[ $startBASE -le 45 && $endBASE -ge 45 ]]
	then
		echo "run BASE 45";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.01 -eN .01200000000000000000 1 > $directory/raw/neutral/BASE45.txt &
	fi
	if [[ $startBASE -le 46 && $endBASE -ge 46 ]]
	then
		echo "run BASE 46";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.005 -eN .01040000000000000000 1 > $directory/raw/neutral/BASE46.txt &
	fi
	if [[ $startBASE -le 47 && $endBASE -ge 47 ]]
	then
		echo "run BASE 47";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.005 -eN .01100000000000000000 1 > $directory/raw/neutral/BASE47.txt &
	fi
	if [[ $startBASE -le 48 && $endBASE -ge 48 ]]
	then
		echo "run BASE 48";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .01000000000000000000 0.005 -eN .01200000000000000000 1 > $directory/raw/neutral/BASE48.txt &
	fi

	if [[ $startBASE -le 49 && $endBASE -ge 49 ]]
	then
		echo "run BASE 49";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.5 -eN .00440000000000000000 1 > $directory/raw/neutral/BASE49.txt &
	fi
	if [[ $startBASE -le 50 && $endBASE -ge 50 ]]
	then
		echo "run BASE 50";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.5 -eN .00500000000000000000 1 > $directory/raw/neutral/BASE50.txt &
	fi
	if [[ $startBASE -le 51 && $endBASE -ge 51 ]]
	then
		echo "run BASE 51";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.5 -eN .00600000000000000000 1 > $directory/raw/neutral/BASE51.txt &
	fi
	if [[ $startBASE -le 52 && $endBASE -ge 52 ]]
	then
		echo "run BASE 52";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.1 -eN .00440000000000000000 1 > $directory/raw/neutral/BASE52.txt &
	fi
	if [[ $startBASE -le 53 && $endBASE -ge 53 ]]
	then
		echo "run BASE 53";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.1 -eN .00500000000000000000 1 > $directory/raw/neutral/BASE53.txt &
	fi
	if [[ $startBASE -le 54 && $endBASE -ge 54 ]]
	then
		echo "run BASE 54";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.1 -eN .00600000000000000000 1 > $directory/raw/neutral/BASE54.txt &
	fi

	if [[ $startBASE -le 55 && $endBASE -ge 55 ]]
	then
		echo "run BASE 55";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.01 -eN .00440000000000000000 1 > $directory/raw/neutral/BASE55.txt &
	fi
	if [[ $startBASE -le 56 && $endBASE -ge 56 ]]
	then
		echo "run BASE 56";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.01 -eN .00500000000000000000 1 > $directory/raw/neutral/BASE56.txt &
	fi
	if [[ $startBASE -le 57 && $endBASE -ge 57 ]]
	then
		echo "run BASE 57";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.01 -eN .00600000000000000000 1 > $directory/raw/neutral/BASE57.txt &
	fi
	if [[ $startBASE -le 58 && $endBASE -ge 58 ]]
	then
		echo "run BASE 58";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.005 -eN .00440000000000000000 1 > $directory/raw/neutral/BASE58.txt &
	fi
	if [[ $startBASE -le 59 && $endBASE -ge 59 ]]
	then
		echo "run BASE 59";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.005 -eN .00500000000000000000 1 > $directory/raw/neutral/BASE59.txt &
	fi
	if [[ $startBASE -le 60 && $endBASE -ge 60 ]]
	then
		echo "run BASE 60";
		./msdir/ms $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .00400000000000000000 0.005 -eN .00600000000000000000 1 > $directory/raw/neutral/BASE60.txt &
	fi

	if [[ $startBASE -le 61 && $endBASE -ge 61 ]]
	then
		echo "run BASE 61";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.003 1 2 -en 0.003 2 1 > $directory/raw/neutral/BASE61.txt &
	fi
	if [[ $startBASE -le 62 && $endBASE -ge 62 ]]
	then
		echo "run BASE 62";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.005 1 2 -en 0.005 2 1 > $directory/raw/neutral/BASE62.txt &
	fi
	if [[ $startBASE -le 63 && $endBASE -ge 63 ]]
	then
		echo "run BASE 63";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.01 1 2 -en 0.01 2 1 > $directory/raw/neutral/BASE63.txt &
	fi
	if [[ $startBASE -le 64 && $endBASE -ge 64 ]]
	then
		echo "run BASE 64";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.05 1 2 -en 0.05 2 1 > $directory/raw/neutral/BASE64.txt &
	fi
	if [[ $startBASE -le 65 && $endBASE -ge 65 ]]
	then
		echo "run BASE 65";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.1 1 2 -en 0.1 2 1 > $directory/raw/neutral/BASE65.txt &
	fi
	if [[ $startBASE -le 66 && $endBASE -ge 66 ]]
	then
		echo "run BASE 66";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.5 1 2 -en 0.5 2 1 > $directory/raw/neutral/BASE66.txt &
	fi

	if [[ $startBASE -le 67 && $endBASE -ge 67 ]]
	then
		echo "run BASE 67";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 1 1 2 -en 1 2 1 > $directory/raw/neutral/BASE67.txt &
	fi
	if [[ $startBASE -le 68 && $endBASE -ge 68 ]]
	then
		echo "run BASE 68";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 1.5 1 2 -en 1.5 2 1 > $directory/raw/neutral/BASE68.txt &
	fi
	if [[ $startBASE -le 69 && $endBASE -ge 69 ]]
	then
		echo "run BASE 69";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 2 1 2 -en 2 2 1 > $directory/raw/neutral/BASE69.txt &
	fi
	if [[ $startBASE -le 70 && $endBASE -ge 70 ]]
	then
		echo "run BASE 70";
		./msdir/ms $individuals $numberOfPopulations -I 2 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 3 1 2 -en 3 2 1 > $directory/raw/neutral/BASE70.txt &
	fi
	if [[ $startBASE -le 71 && $endBASE -ge 71 ]]
	then
		echo "run BASE 71";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE71.txt &
	fi
	if [[ $startBASE -le 72 && $endBASE -ge 72 ]]
	then
		echo "run BASE 72";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE72.txt &
	fi

	if [[ $startBASE -le 73 && $endBASE -ge 73 ]]
	then
		echo "run BASE 73";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE73.txt &
	fi
	if [[ $startBASE -le 74 && $endBASE -ge 74 ]]
	then
		echo "run BASE 74";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE74.txt &
	fi
	if [[ $startBASE -le 75 && $endBASE -ge 75 ]]
	then
		echo "run BASE 75";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE75.txt &
	fi
	if [[ $startBASE -le 76 && $endBASE -ge 76 ]]
	then
		echo "run BASE 76";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE76.txt &
	fi
	if [[ $startBASE -le 77 && $endBASE -ge 77 ]]
	then
		echo "run BASE 77";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE77.txt &
	fi
	if [[ $startBASE -le 78 && $endBASE -ge 78 ]]
	then
		echo "run BASE 78";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE78.txt &
	fi

	if [[ $startBASE -le 79 && $endBASE -ge 79 ]]
	then
		echo "run BASE 79";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE79.txt &
	fi
	if [[ $startBASE -le 80 && $endBASE -ge 80 ]]
	then
		echo "run BASE 80";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE80.txt &
	fi
	if [[ $startBASE -le 81 && $endBASE -ge 81 ]]
	then
		echo "run BASE 81";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE81.txt &
	fi
	if [[ $startBASE -le 82 && $endBASE -ge 82 ]]
	then
		echo "run BASE 82";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE82.txt &
	fi
	if [[ $startBASE -le 83 && $endBASE -ge 83 ]]
	then
		echo "run BASE 83";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE83.txt &
	fi
	if [[ $startBASE -le 84 && $endBASE -ge 84 ]]
	then
		echo "run BASE 84";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE84.txt &
	fi

	if [[ $startBASE -le 85 && $endBASE -ge 85 ]]
	then
		echo "run BASE 85";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE85.txt &
	fi
	if [[ $startBASE -le 86 && $endBASE -ge 86 ]]
	then
		echo "run BASE 86";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE86.txt &
	fi
	if [[ $startBASE -le 87 && $endBASE -ge 87 ]]
	then
		echo "run BASE 87";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE87.txt &
	fi
	if [[ $startBASE -le 88 && $endBASE -ge 88 ]]
	then
		echo "run BASE 88";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE88.txt &
	fi
	if [[ $startBASE -le 89 && $endBASE -ge 89 ]]
	then
		echo "run BASE 89";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE89.txt &
	fi
	if [[ $startBASE -le 90 && $endBASE -ge 90 ]]
	then
		echo "run BASE 90";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE90.txt &
	fi

	if [[ $startBASE -le 91 && $endBASE -ge 91 ]]
	then
		echo "run BASE 91";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/neutral/BASE91.txt &
	fi
	if [[ $startBASE -le 92 && $endBASE -ge 92 ]]
	then
		echo "run BASE 92";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 2 > $directory/raw/neutral/BASE92.txt &
	fi
	if [[ $startBASE -le 93 && $endBASE -ge 93 ]]
	then
		echo "run BASE 93";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 4 > $directory/raw/neutral/BASE93.txt &
	fi
	if [[ $startBASE -le 94 && $endBASE -ge 94 ]]
	then
		echo "run BASE 94";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 8 > $directory/raw/neutral/BASE94.txt &
	fi
	if [[ $startBASE -le 95 && $endBASE -ge 95 ]]
	then
		echo "run BASE 95";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 10 > $directory/raw/neutral/BASE95.txt &
	fi
	if [[ $startBASE -le 96 && $endBASE -ge 96 ]]
	then
		echo "run BASE 96";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 20 > $directory/raw/neutral/BASE96.txt &
	fi
	if [[ $startBASE -le 97 && $endBASE -ge 97 ]]
	then
		echo "run BASE 97";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 2 > $directory/raw/neutral/BASE97.txt &
	fi
	if [[ $startBASE -le 98 && $endBASE -ge 98 ]]
	then
		echo "run BASE 98";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 4 > $directory/raw/neutral/BASE98.txt &
	fi
	if [[ $startBASE -le 99 && $endBASE -ge 99 ]]
	then
		echo "run BASE 99";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 8 > $directory/raw/neutral/BASE99.txt &
	fi
	if [[ $startBASE -le 100 && $endBASE -ge 100 ]]
	then
		echo "run BASE 100";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 10 > $directory/raw/neutral/BASE100.txt &
	fi
	if [[ $startBASE -le 101 && $endBASE -ge 101 ]]
	then
		echo "run BASE 101";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 20 > $directory/raw/neutral/BASE101.txt &
	fi
	wait
done
################################################################################################################################################################


for i in `seq 0 $threads $((endTESTIn-startTESTIn))`
do
	startTEST=$((startTESTIn+i))
	endTEST=$((startTESTIn+threads+i-1))
	if [[ $endTEST -gt $endTESTIn ]]
	then
		endTEST=$((endTESTIn))
	fi
	
	################
	## TEST files ##
	################
	if [[ $startTEST -gt 0 ]]
	then
		echo starting TEST threads
		echo "start ${startTEST}"
		echo "end ${endTEST}"
	fi
	################################################################################################################################################################
	if [[ $startTEST -le 1 && $endTEST -ge 1 ]]
	then
		echo "run TEST 1";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory1.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 > $directory/raw/hard/TEST1.txt &
	fi
	if [[ $startTEST -le 2 && $endTEST -ge 2 ]]
	then
		echo "run TEST 2";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory2.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10100000000000000000 1 > $directory/raw/hard/TEST2.txt &
	fi
	if [[ $startTEST -le 3 && $endTEST -ge 3 ]]
	then
		echo "run TEST 3";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory3.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10200000000000000000 1 > $directory/raw/hard/TEST3.txt &
	fi
	if [[ $startTEST -le 4 && $endTEST -ge 4 ]]
	then
		echo "run TEST 4";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory4.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.1 -eN .10040000000000000000 1 > $directory/raw/hard/TEST4.txt &
	fi
	if [[ $startTEST -le 5 && $endTEST -ge 5 ]]
	then
		echo "run TEST 5";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory5.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.1 -eN .10100000000000000000 1 > $directory/raw/hard/TEST5.txt &
	fi
	if [[ $startTEST -le 6 && $endTEST -ge 6 ]]
	then
		echo "run TEST 6";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory6.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.1 -eN .10200000000000000000 1 > $directory/raw/hard/TEST6.txt &
	fi

	if [[ $startTEST -le 7 && $endTEST -ge 7 ]]
	then
		echo "run TEST 7";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory7.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.01 -eN .10040000000000000000 1 > $directory/raw/hard/TEST7.txt &
	fi
	if [[ $startTEST -le 8 && $endTEST -ge 8 ]]
	then
		echo "run TEST 8";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory8.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.01 -eN .10100000000000000000 1 > $directory/raw/hard/TEST8.txt &
	fi
	if [[ $startTEST -le 9 && $endTEST -ge 9 ]]
	then
		echo "run TEST 9";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory9.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.01 -eN .10200000000000000000 1 > $directory/raw/hard/TEST9.txt &
	fi
	if [[ $startTEST -le 10 && $endTEST -ge 10 ]]
	then
		echo "run TEST 10";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory10.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.005 -eN .10040000000000000000 1 > $directory/raw/hard/TEST10.txt & 
	fi
	if [[ $startTEST -le 11 && $endTEST -ge 11 ]]
	then
		echo "run TEST 11";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory11.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.005 -eN .10100000000000000000 1 > $directory/raw/hard/TEST11.txt &
	fi
	if [[ $startTEST -le 12 && $endTEST -ge 12 ]]
	then
		echo "run TEST 12";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory12.txt 1000 -t 2000 -r 2000 2000 -eN .10000000000000000000 0.005 -eN .10200000000000000000 1 > $directory/raw/hard/TEST12.txt &
	fi

	if [[ $startTEST -le 13 && $endTEST -ge 13 ]]
	then
		echo "run TEST 13";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory13.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.5 -eN .02040000000000000000 1 > $directory/raw/hard/TEST13.txt & 
	fi
	if [[ $startTEST -le 14 && $endTEST -ge 14 ]]
	then
		echo "run TEST 14";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory14.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.5 -eN .02100000000000000000 1 > $directory/raw/hard/TEST14.txt &
	fi
	if [[ $startTEST -le 15 && $endTEST -ge 15 ]]
	then
		echo "run TEST 15";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory15.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.5 -eN .02200000000000000000 1 > $directory/raw/hard/TEST15.txt &
	fi
	if [[ $startTEST -le 16 && $endTEST -ge 16 ]]
	then
		echo "run TEST 16";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory16.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.1 -eN .02040000000000000000 1 > $directory/raw/hard/TEST16.txt &
	fi
	if [[ $startTEST -le 17 && $endTEST -ge 17 ]]
	then
		echo "run TEST 17";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory17.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.1 -eN .02100000000000000000 1 > $directory/raw/hard/TEST17.txt &
	fi
	if [[ $startTEST -le 18 && $endTEST -ge 18 ]]
	then
		echo "run TEST 18";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory18.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.1 -eN .02200000000000000000 1 > $directory/raw/hard/TEST18.txt &
	fi

	if [[ $startTEST -le 19 && $endTEST -ge 19 ]]
	then
		echo "run TEST 19";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory19.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.01 -eN .02040000000000000000 1 > $directory/raw/hard/TEST19.txt &
	fi
	if [[ $startTEST -le 20 && $endTEST -ge 20 ]]
	then
		echo "run TEST 20";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory20.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.01 -eN .02100000000000000000 1 > $directory/raw/hard/TEST20.txt &
	fi
	if [[ $startTEST -le 21 && $endTEST -ge 21 ]]
	then
		echo "run TEST 21";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory21.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.01 -eN .02200000000000000000 1 > $directory/raw/hard/TEST21.txt &
	fi
	if [[ $startTEST -le 22 && $endTEST -ge 22 ]]
	then
		echo "run TEST 22";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory22.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.005 -eN .02040000000000000000 1 > $directory/raw/hard/TEST22.txt &
	fi
	if [[ $startTEST -le 23 && $endTEST -ge 23 ]]
	then
		echo "run TEST 23";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory23.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.005 -eN .02100000000000000000 1 > $directory/raw/hard/TEST23.txt &
	fi
	if [[ $startTEST -le 24 && $endTEST -ge 24 ]]
	then
		echo "run TEST 24";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory24.txt 1000 -t 2000 -r 2000 2000 -eN .02000000000000000000 0.005 -eN .02200000000000000000 1 > $directory/raw/hard/TEST24.txt &
	fi

	if [[ $startTEST -le 25 && $endTEST -ge 25 ]]
	then
		echo "run TEST 25";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory25.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.5 -eN .01540000000000000000 1 > $directory/raw/hard/TEST25.txt &
	fi
	if [[ $startTEST -le 26 && $endTEST -ge 26 ]]
	then
		echo "run TEST 26";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory26.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.5 -eN .01600000000000000000 1 > $directory/raw/hard/TEST26.txt &
	fi
	if [[ $startTEST -le 27 && $endTEST -ge 27 ]]
	then
		echo "run TEST 27";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory27.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.5 -eN .01700000000000000000 1 > $directory/raw/hard/TEST27.txt &
	fi
	if [[ $startTEST -le 28 && $endTEST -ge 28 ]]
	then
		echo "run TEST 28";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory28.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.1 -eN .01540000000000000000 1 > $directory/raw/hard/TEST28.txt &
	fi
	if [[ $startTEST -le 29 && $endTEST -ge 29 ]]
	then
		echo "run TEST 29";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory29.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.1 -eN .01600000000000000000 1 > $directory/raw/hard/TEST29.txt &
	fi
	if [[ $startTEST -le 30 && $endTEST -ge 30 ]]
	then
		echo "run TEST 30";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory30.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.1 -eN .01700000000000000000 1 > $directory/raw/hard/TEST30.txt &
	fi

	if [[ $startTEST -le 31 && $endTEST -ge 31 ]]
	then
		echo "run TEST 31";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory31.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.01 -eN .01540000000000000000 1 > $directory/raw/hard/TEST31.txt &
	fi
	if [[ $startTEST -le 32 && $endTEST -ge 32 ]]
	then
		echo "run TEST 32";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory32.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.01 -eN .01600000000000000000 1 > $directory/raw/hard/TEST32.txt &
	fi
	if [[ $startTEST -le 33 && $endTEST -ge 33 ]]
	then
		echo "run TEST 33";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory33.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.01 -eN .01700000000000000000 1 > $directory/raw/hard/TEST33.txt &
	fi
	if [[ $startTEST -le 34 && $endTEST -ge 34 ]]
	then
		echo "run TEST 34";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory34.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.005 -eN .01540000000000000000 1 > $directory/raw/hard/TEST34.txt &
	fi
	if [[ $startTEST -le 35 && $endTEST -ge 35 ]]
	then
		echo "run TEST 35";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory35.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.005 -eN .01600000000000000000 1 > $directory/raw/hard/TEST35.txt &
	fi
	if [[ $startTEST -le 36 && $endTEST -ge 36 ]]
	then
		echo "run TEST 36";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory36.txt 1000 -t 2000 -r 2000 2000 -eN .01500000000000000000 0.005 -eN .01700000000000000000 1 > $directory/raw/hard/TEST36.txt &
	fi

	if [[ $startTEST -le 37 && $endTEST -ge 37 ]]
	then
		echo "run TEST 37";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory37.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.5 -eN .01040000000000000000 1 > $directory/raw/hard/TEST37.txt &
	fi
	if [[ $startTEST -le 38 && $endTEST -ge 38 ]]
	then
		echo "run TEST 38";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory38.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.5 -eN .01100000000000000000 1 > $directory/raw/hard/TEST38.txt &
	fi
	if [[ $startTEST -le 39 && $endTEST -ge 39 ]]
	then
		echo "run TEST 39";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory39.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.5 -eN .01200000000000000000 1 > $directory/raw/hard/TEST39.txt &
	fi
	if [[ $startTEST -le 40 && $endTEST -ge 40 ]]
	then
		echo "run TEST 40";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory40.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.1 -eN .01040000000000000000 1 > $directory/raw/hard/TEST40.txt &
	fi
	if [[ $startTEST -le 41 && $endTEST -ge 41 ]]
	then
		echo "run TEST 41";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory41.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.1 -eN .01100000000000000000 1 > $directory/raw/hard/TEST41.txt &
	fi
	if [[ $startTEST -le 42 && $endTEST -ge 42 ]]
	then
		echo "run TEST 42";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory42.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.1 -eN .01200000000000000000 1 > $directory/raw/hard/TEST42.txt &
	fi

	if [[ $startTEST -le 43 && $endTEST -ge 43 ]]
	then
		echo "run TEST 43";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory43.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.01 -eN .01040000000000000000 1 > $directory/raw/hard/TEST43.txt &
	fi
	if [[ $startTEST -le 44 && $endTEST -ge 44 ]]
	then
		echo "run TEST 44";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory44.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.01 -eN .01100000000000000000 1 > $directory/raw/hard/TEST44.txt &
	fi
	if [[ $startTEST -le 45 && $endTEST -ge 45 ]]
	then
		echo "run TEST 45";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory45.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.01 -eN .01200000000000000000 1 > $directory/raw/hard/TEST45.txt &
	fi
	if [[ $startTEST -le 46 && $endTEST -ge 46 ]]
	then
		echo "run TEST 46";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory46.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.005 -eN .01040000000000000000 1 > $directory/raw/hard/TEST46.txt &
	fi
	if [[ $startTEST -le 47 && $endTEST -ge 47 ]]
	then
		echo "run TEST 47";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory47.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.005 -eN .01100000000000000000 1 > $directory/raw/hard/TEST47.txt &
	fi
	if [[ $startTEST -le 48 && $endTEST -ge 48 ]]
	then
		echo "run TEST 48";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory48.txt 1000 -t 2000 -r 2000 2000 -eN .01000000000000000000 0.005 -eN .01200000000000000000 1 > $directory/raw/hard/TEST48.txt &
	fi

	if [[ $startTEST -le 49 && $endTEST -ge 49 ]]
	then
		echo "run TEST 49";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory49.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.5 -eN .00440000000000000000 1 > $directory/raw/hard/TEST49.txt  &
	fi
	if [[ $startTEST -le 50 && $endTEST -ge 50 ]]
	then
		echo "run TEST 50";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory50.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.5 -eN .00500000000000000000 1 > $directory/raw/hard/TEST50.txt  &
	fi
	if [[ $startTEST -le 51 && $endTEST -ge 51 ]]
	then
		echo "run TEST 51";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory51.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.5 -eN .00600000000000000000 1 > $directory/raw/hard/TEST51.txt  &
	fi
	if [[ $startTEST -le 52 && $endTEST -ge 52 ]]
	then
		echo "run TEST 52";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory52.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.1 -eN .00440000000000000000 1 > $directory/raw/hard/TEST52.txt &
	fi
	if [[ $startTEST -le 53 && $endTEST -ge 53 ]]
	then
		echo "run TEST 53";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory53.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.1 -eN .00500000000000000000 1 > $directory/raw/hard/TEST53.txt &
	fi
	if [[ $startTEST -le 54 && $endTEST -ge 54 ]]
	then
		echo "run TEST 54";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory54.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.1 -eN .00600000000000000000 1 > $directory/raw/hard/TEST54.txt &
	fi

	if [[ $startTEST -le 55 && $endTEST -ge 55 ]]
	then
		echo "run TEST 55";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory55.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.01 -eN .00440000000000000000 1 > $directory/raw/hard/TEST55.txt &
	fi
	if [[ $startTEST -le 56 && $endTEST -ge 56 ]]
	then
		echo "run TEST 56";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory56.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.01 -eN .00500000000000000000 1 > $directory/raw/hard/TEST56.txt &
	fi
	if [[ $startTEST -le 57 && $endTEST -ge 57 ]]
	then
		echo "run TEST 57";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory57.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.01 -eN .00600000000000000000 1 > $directory/raw/hard/TEST57.txt &
	fi
	if [[ $startTEST -le 58 && $endTEST -ge 58 ]]
	then
		echo "run TEST 58";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory58.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.005 -eN .00440000000000000000 1 > $directory/raw/hard/TEST58.txt &
	fi
	if [[ $startTEST -le 59 && $endTEST -ge 59 ]]
	then
		echo "run TEST 59";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory59.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.005 -eN .00500000000000000000 1 > $directory/raw/hard/TEST59.txt &
	fi
	if [[ $startTEST -le 60 && $endTEST -ge 60 ]]
	then
		echo "run TEST 60";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory60.txt 1000 -t 2000 -r 2000 2000 -eN .00400000000000000000 0.005 -eN .00600000000000000000 1 > $directory/raw/hard/TEST60.txt &
	fi

	if [[ $startTEST -le 61 && $endTEST -ge 61 ]]
	then
		echo "run TEST 61";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.003 1 2 -en 0.003 2 1 > $directory/raw/hard/TEST61.txt &
	fi
	if [[ $startTEST -le 62 && $endTEST -ge 62 ]]
	then
		echo "run TEST 62";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.005 1 2 -en 0.005 2 1 > $directory/raw/hard/TEST62.txt &
	fi
	if [[ $startTEST -le 63 && $endTEST -ge 63 ]]
	then
		echo "run TEST 63";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.01 1 2 -en 0.01 2 1 > $directory/raw/hard/TEST63.txt &
	fi
	if [[ $startTEST -le 64 && $endTEST -ge 64 ]]
	then
		echo "run TEST 64";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.05 1 2 -en 0.05 2 1 > $directory/raw/hard/TEST64.txt &
	fi
	if [[ $startTEST -le 65 && $endTEST -ge 65 ]]
	then
		echo "run TEST 65";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.1 1 2 -en 0.1 2 1 > $directory/raw/hard/TEST65.txt &
	fi
	if [[ $startTEST -le 66 && $endTEST -ge 66 ]]
	then
		echo "run TEST 66";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 0.5 1 2 -en 0.5 2 1 > $directory/raw/hard/TEST66.txt &
	fi

	if [[ $startTEST -le 67 && $endTEST -ge 67 ]]
	then
		echo "run TEST 67";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 1 1 2 -en 1 2 1 > $directory/raw/hard/TEST67.txt &
	fi
	if [[ $startTEST -le 68 && $endTEST -ge 68 ]]
	then
		echo "run TEST 68";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 1.5 1 2 -en 1.5 2 1 > $directory/raw/hard/TEST68.txt &
	fi
	if [[ $startTEST -le 69 && $endTEST -ge 69 ]]
	then
		echo "run TEST 69";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 2 1 2 -en 2 2 1 > $directory/raw/hard/TEST69.txt &
	fi
	if [[ $startTEST -le 70 && $endTEST -ge 70 ]]
	then
		echo "run TEST 70";
		./msseldir/mssel $individuals $numberOfPopulations 0 $individuals ./trajectory_files/trajectory_continent_island.txt 1000 -I 2 0 0 0 20 0.0 -en 0 2 0.05 -em 0 2 1 3 -t 2000 -r 2000 2000 -ej 3 1 2 -en 3 2 1 > $directory/raw/hard/TEST70.txt &
	fi
	if [[ $startTEST -le 71 && $endTEST -ge 71 ]]
	then
		echo "run TEST 71";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 2 > $directory/raw/hard/TEST71.txt &
	fi
	if [[ $startTEST -le 72 && $endTEST -ge 72 ]]
	then
		echo "run TEST 72";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 4 > $directory/raw/hard/TEST72.txt &
	fi

	if [[ $startTEST -le 73 && $endTEST -ge 73 ]]
	then
		echo "run TEST 73";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 8 > $directory/raw/hard/TEST73.txt &
	fi
	if [[ $startTEST -le 74 && $endTEST -ge 74 ]]
	then
		echo "run TEST 74";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 10 > $directory/raw/hard/TEST74.txt &
	fi
	if [[ $startTEST -le 75 && $endTEST -ge 75 ]]
	then
		echo "run TEST 75";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 20 > $directory/raw/hard/TEST75.txt &
	fi
	if [[ $startTEST -le 76 && $endTEST -ge 76 ]]
	then
		echo "run TEST 76";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 40 > $directory/raw/hard/TEST76.txt &
	fi
	if [[ $startTEST -le 77 && $endTEST -ge 77 ]]
	then
		echo "run TEST 77";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 950 1050 100 > $directory/raw/hard/TEST77.txt &
	fi
	if [[ $startTEST -le 78 && $endTEST -ge 78 ]]
	then
		echo "run TEST 78";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 2 > $directory/raw/hard/TEST78.txt &
	fi

	if [[ $startTEST -le 79 && $endTEST -ge 79 ]]
	then
		echo "run TEST 79";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 4 > $directory/raw/hard/TEST79.txt &
	fi
	if [[ $startTEST -le 80 && $endTEST -ge 80 ]]
	then
		echo "run TEST 80";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 8 > $directory/raw/hard/TEST80.txt &
	fi
	if [[ $startTEST -le 81 && $endTEST -ge 81 ]]
	then
		echo "run TEST 81";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 10 > $directory/raw/hard/TEST81.txt &
	fi
	if [[ $startTEST -le 82 && $endTEST -ge 82 ]]
	then
		echo "run TEST 82";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 20 > $directory/raw/hard/TEST82.txt &
	fi
	if [[ $startTEST -le 83 && $endTEST -ge 83 ]]
	then
		echo "run TEST 83";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 40 > $directory/raw/hard/TEST83.txt &
	fi
	if [[ $startTEST -le 84 && $endTEST -ge 84 ]]
	then
		echo "run TEST 84";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 1 900 1100 100 > $directory/raw/hard/TEST84.txt &
	fi

	if [[ $startTEST -le 85 && $endTEST -ge 85 ]]
	then
		echo "run TEST 85";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 2 950 1050 2 1450 1550 2 > $directory/raw/hard/TEST85.txt &
	fi
	if [[ $startTEST -le 86 && $endTEST -ge 86 ]]
	then
		echo "run TEST 86";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 4 950 1050 4 1450 1550 4 > $directory/raw/hard/TEST86.txt &
	fi
	if [[ $startTEST -le 87 && $endTEST -ge 87 ]]
	then
		echo "run TEST 87";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 8 950 1050 8 1450 1550 8 > $directory/raw/hard/TEST87.txt &
	fi
	if [[ $startTEST -le 88 && $endTEST -ge 88 ]]
	then
		echo "run TEST 88";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 10 950 1050 10 1450 1550 10 > $directory/raw/hard/TEST88.txt &
	fi
	if [[ $startTEST -le 89 && $endTEST -ge 89 ]]
	then
		echo "run TEST 89";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 20 950 1050 20 1450 1550 20 > $directory/raw/hard/TEST89.txt &
	fi
	if [[ $startTEST -le 90 && $endTEST -ge 90 ]]
	then
		echo "run TEST 90";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 40 950 1050 40 1450 1550 40 > $directory/raw/hard/TEST90.txt &
	fi

	if [[ $startTEST -le 91 && $endTEST -ge 91 ]]
	then
		echo "run TEST 91";
		./msHOT/msHOT $individuals $numberOfPopulations -t 2000 -r 2000 2000 -eN .10000000000000000000 0.5 -eN .10040000000000000000 1 -v 3 450 550 100 950 1050 100 1450 1550 100 > $directory/raw/hard/TEST91.txt &
	fi
	if [[ $startTEST -le 92 && $endTEST -ge 92 ]]
	then
		echo "run TEST 92";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 50000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_2.txt > $directory/raw/hard/TEST92.txt &
	fi
	if [[ $startTEST -le 93 && $endTEST -ge 93 ]]
	then
		echo "run TEST 93";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 50000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_4.txt > $directory/raw/hard/TEST93.txt &
	fi
	if [[ $startTEST -le 94 && $endTEST -ge 94 ]]
	then
		echo "run TEST 94";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 50000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_8.txt > $directory/raw/hard/TEST94.txt &
	fi
	if [[ $startTEST -le 95 && $endTEST -ge 95 ]]
	then
		echo "run TEST 95";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 50000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_10.txt > $directory/raw/hard/TEST95.txt &
	fi
	if [[ $startTEST -le 96 && $endTEST -ge 96 ]]
	then
		echo "run TEST 96";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 50000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_20.txt > $directory/raw/hard/TEST96.txt &
	fi
	if [[ $startTEST -le 97 && $endTEST -ge 97 ]]
	then
		echo "run TEST 97";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 30000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_2.txt > $directory/raw/hard/TEST97.txt &
	fi
	if [[ $startTEST -le 98 && $endTEST -ge 98 ]]
	then
		echo "run TEST 98";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 30000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_4.txt > $directory/raw/hard/TEST98.txt &
	fi
	if [[ $startTEST -le 99 && $endTEST -ge 99 ]]
	then
		echo "run TEST 99";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 30000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_8.txt > $directory/raw/hard/TEST99.txt &
	fi
	if [[ $startTEST -le 100 && $endTEST -ge 100 ]]
	then
		echo "run TEST 100";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 30000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_10.txt > $directory/raw/hard/TEST100.txt &
	fi
	if [[ $startTEST -le 101 && $endTEST -ge 101 ]]
	then
		echo "run TEST 101";
		./mbs/mbs $individuals -t 0.02 -r 0.02 -s 100000 30000 -f 1 $numberOfPopulations ./mbsFiles/traj -h ./mbsFiles/rechot_47500_52500_20.txt > $directory/raw/hard/TEST101.txt &
	fi
	wait
done
################################################################################################################################################################
echo succesfully generated all raw files with
