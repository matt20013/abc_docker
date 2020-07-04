#!/bin/bash

#find . -maxdepth 1 -type f -name "*.txt"

#shopt -s globstar
#for i in **/*.abc; do # Whitespace-safe and recursive
#    ABC_FILENAME=$(echo $i | cut -f 1 -d '.')
#    echo $ABC_FILENAME
#done

for i in abcs/*.abc; do # Whitespace-safe but not recursive.
    echo $i
    export ABC_PATH=$i
    export ABC_FILE="${i##*/}"
    export ABC_FILENAME="${ABC_FILE%.*}"
    echo $ABC_FILENAME
    python generate_mp3.py ../abcs/${ABC_FILENAME}.abc ../mp3s/
done
