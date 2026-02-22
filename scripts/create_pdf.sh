#!/bin/bash

ABC_DIR="${ABC_DIR:-/abcs}"
PDF_DIR="${PDF_DIR:-/pdfs}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

if [[ -z "$ABC_FILENAME" ]]; then
   echo "Empty ABC_FILENAME please set"
   exit 1
fi

# Check for abcm2ps
if ! command -v abcm2ps &> /dev/null; then
    echo "abcm2ps could not be found"
    exit 1
fi

if [[ -z "$ABC_FONTS_PATH" ]]; then
   echo "ABC_FONTS_PATH not set, defaulting to /Library/Fonts"
   ABC_FONTS_PATH=/Library/Fonts
fi

if test -f "$ABC_DIR/${ABC_FILENAME}.fmt"; then
    abcm2ps -O "$PDF_DIR/${ABC_FILENAME}_raw.ps" -F "$ABC_DIR/${ABC_FILENAME}.fmt" "$ABC_DIR/${ABC_FILENAME}.abc"
elif test -f "$ABC_DIR/default.fmt"; then
    echo WARNING "$ABC_DIR/${ABC_FILENAME}.fmt" DOES NOT EXIST. Using default.fmt from ABC_DIR
    abcm2ps -O "$PDF_DIR/${ABC_FILENAME}_raw.ps" -F "$ABC_DIR/default.fmt" "$ABC_DIR/${ABC_FILENAME}.abc"
else
    echo WARNING "$ABC_DIR/${ABC_FILENAME}.fmt" and "$ABC_DIR/default.fmt" DO NOT EXIST. Using internal default.fmt
    abcm2ps -O "$PDF_DIR/${ABC_FILENAME}_raw.ps" -F "/scripts/default.fmt" "$ABC_DIR/${ABC_FILENAME}.abc"
fi

RET_CODE=$?
if [ $RET_CODE -eq 0 ] && [ -s "$PDF_DIR/${ABC_FILENAME}_raw.ps" ]; then
    echo "$PDF_DIR/${ABC_FILENAME}_raw.ps" created successfully
elif [ -n "$FORCE_CREATION" ] && [ "$FORCE_CREATION" != "0" ] && [ -s "$PDF_DIR/${ABC_FILENAME}_raw.ps" ]; then
    echo "WARNING: abcm2ps exited with code $RET_CODE but FORCE_CREATION is set. Proceeding..."
else
    echo FAILED to create "$PDF_DIR/${ABC_FILENAME}_raw.ps"
    exit 1
fi

tclsh "$SCRIPT_DIR/abcmaddidx.tcl" "$PDF_DIR/${ABC_FILENAME}_raw.ps" "$PDF_DIR/${ABC_FILENAME}.ps"
#rm pdfs/${ABC_FILENAME}_raw.ps
ps2pdf -sFONTPATH=${ABC_FONTS_PATH} "$PDF_DIR/${ABC_FILENAME}.ps" "$PDF_DIR/${ABC_FILENAME}.pdf"
#rm pdfs/${ABC_FILENAME}.ps
exit 0
