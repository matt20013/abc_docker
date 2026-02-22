#!/bin/bash
ABC_DIR="${ABC_DIR:-../abcs}"

for i in "$ABC_DIR"/*.jpg; do # Whitespace-safe but not recursive.
    [ -e "$i" ] || continue
    echo "$i"
    export JPG_FILENAME="${i%.*}"
    convert "${JPG_FILENAME}.jpg" "${JPG_FILENAME}.eps"
done
