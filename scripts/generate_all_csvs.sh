#!/bin/bash

ABC_DIR="${ABC_DIR:-../abcs}"
CSV_DIR="${CSV_DIR:-../csvs}"

for i in "$ABC_DIR"/*.abc; do # Whitespace-safe but not recursive.
    [ -e "$i" ] || continue
    echo "$i"
    export ABC_PATH="$i"
    export ABC_FILE="${i##*/}"
    export ABC_FILENAME="${ABC_FILE%.*}"
    echo "$ABC_FILENAME"
    python generate_csv.py "$i" "$CSV_DIR/${ABC_FILENAME}.csv"
done
