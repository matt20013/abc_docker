#!/bin/bash
if [[ -z "$ABC_FILENAME" ]]; then
   echo "Empty ABC_FILENAME please set"
fi

if [[ -z "$ABC_FONTS_PATH" ]]; then
   echo "ABC_FONTS_PATH not set, defaulting to /Libary/Fonts"
   ABC_FONTS_PATH=/Library/Fonts
fi

if test -f ../abcs${ABC_FILENAME}.fmt; then
    abcm2ps -O ../pdfs/${ABC_FILENAME}_raw.ps -F ../abcs${ABC_FILENAME}.fmt ../abcs/${ABC_FILENAME}.abc
#else
#    echo WARNING ${ABC_FILENAME}.fmt DOES NOT EXIST. Creating PS file WITHOUT format file
#    ../abcm2ps/abcm2ps -O pdfs/${ABC_FILENAME}_raw.ps  abcs/${ABC_FILENAME}.abc   
else
    echo WARNING ../abcs/${ABC_FILENAME}.fmt DOES NOT EXIST. Using default.fmt
    abcm2ps -O ../pdfs/${ABC_FILENAME}_raw.ps -F ../abcs/default.fmt ../abcs/${ABC_FILENAME}.abc
fi

if [ $? -eq 0 ]
then
    echo ../pdfs${ABC_FILENAME}_raw.ps created successfully
else
    echo FAILED to create ../pdfs/${ABC_FILENAME}_raw.ps
    #exit 1
fi

#../abcm2ps/abcm2ps -O pdfs/${ABC_FILENAME}_raw.ps -F ${ABC_FILENAME}.fmt ${ABC_FILENAME}.abc
tclsh abcmaddidx.tcl ../pdfs/${ABC_FILENAME}_raw.ps ../pdfs/${ABC_FILENAME}.ps
#rm pdfs/${ABC_FILENAME}_raw.ps
ps2pdf -sFONTPATH=${ABC_FONTS_PATH} ../pdfs/${ABC_FILENAME}.ps ../pdfs/${ABC_FILENAME}.pdf
#rm pdfs/${ABC_FILENAME}.ps
exit 0
