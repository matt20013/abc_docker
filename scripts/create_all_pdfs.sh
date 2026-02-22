#!/bin/bash
ABC_DIR="${ABC_DIR:-../abcs}"
PDF_DIR="${PDF_DIR:-../pdfs}"
export PDF_DIR

for i in "$ABC_DIR"/*.abc; do # Whitespace-safe but not recursive.
    [ -e "$i" ] || continue
    echo "$i"
    export ABC_PATH="$i"
    export ABC_FILE="${i##*/}"
    export ABC_FILENAME="${ABC_FILE%.*}"
    echo "$ABC_FILENAME"
    ./create_pdf.sh
done
