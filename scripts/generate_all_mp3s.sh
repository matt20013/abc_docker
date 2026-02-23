#!/bin/bash
ABC_DIR="${ABC_DIR:-../abcs}"
MP3_DIR="${MP3_DIR:-../mp3s}"

for i in "$ABC_DIR"/*.abc; do # Whitespace-safe but not recursive.
    [ -e "$i" ] || continue
    echo "$i"
    export ABC_PATH="$i"
    export ABC_FILE="${i##*/}"
    export ABC_FILENAME="${ABC_FILE%.*}"
    echo "$ABC_FILENAME"
    python generate_mp3.py "$i" "$MP3_DIR"
done
