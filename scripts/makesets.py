#!/usr/bin/python 
#Filename: makesets.py
#
# Python Script to create sets from Paul Hardy's Session Tunebook
# See http://www.pghardy.net/concertina/tunebooks/
#
# Created PGH 2009-08-15
# Modified PGH 2009-08-20 (format tidies)
# Modified PGH 2010-09-22 (from Annex file as well as primary)
# Modified PGH 2016-03-08 (TS for session so can have embedded tunes)
# Modified PGH 2017-09-15 (for Windows 10 folder names)

import string,re,sys

def main():
    "Script to create sets from Paul Hardy's Session Tunebook."
    inabcprifilename = "C:\Users\Public\Documents\Music\ABC\PGH_Tunebooks\PGH_Session_Tunebook\pgh_session_tunebook.abc"
    inabcannfilename = "C:\Users\Public\Documents\Music\ABC\PGH_Tunebooks\PGH_Annex_Tunebook\pgh_annex_tunebook.abc"
    indefnfilename = "C:\Users\Public\Documents\Music\ABC\PGH_Tunebooks\PGH_Sets_Tunebook\pgh_sets_tunebook.abct"
    outabcfilename = "C:\Users\Public\Documents\Music\ABC\PGH_Tunebooks\PGH_Sets_Tunebook\pgh_sets_tunebook.abc"
    try:
        indefnfile = open(indefnfilename, 'r')  
    except IOError:
        print("Can\'t open set definitions file for reading. "+indefnfilename)
        sys.exit(0)
    try:
        inabcprifile = open(inabcprifilename, 'r')  
    except IOError:
        print("Can\'t open input primary abc file for reading. "+inabcprifilename)
        sys.exit(0)
    try:
        inabcannfile = open(inabcannfilename, 'r')  
    except IOError:
        print("Can\'t open input annex abc file for reading. "+inabcannfilename)
        sys.exit(0)
    try:
        outabcfile = open(outabcfilename, 'w')  
    except IOError:
        print("Can\'t open output abc file for writing. "+outabcfilename)
        sys.exit(0)
#
# loop for all lines in set definition
    defnlineno = 0
    while 1:
        defnline = indefnfile.readline()
        if not defnline: break
        defnlineno = defnlineno + 1
        if re.search("TS:",defnline):
            thistunename=defnline[2:len(defnline)-1]
            print("'%s'"%thistunename)
            findandcopytune(thistunename,inabcprifile,outabcfile)
            outabcfile.write("")
            continue
        if re.search("TA:",defnline):
            thistunename=defnline[2:len(defnline)-1]
            print("'%s'"%thistunename)
            findandcopytune(thistunename,inabcannfile,outabcfile)
            outabcfile.write("")
            continue
        outabcfile.write(defnline)
    indefnfile.close()
#
# routine to find a given tune and copy it to the output
def findandcopytune(tunename,infile,outfile):
    "Copy one tune from Paul Hardy's Session Tunebook."
    infile.seek(0)
    foundtune = 0
    abclineno=0
    while 1:
        abcline = infile.readline()
        if not abcline: break
        abclineno = abclineno + 1
        if re.search("X:",abcline):
#               print(abcline)
            xline=abcline
        if not re.search("T:",abcline): continue
#           print(abcline)
        if re.search(tunename,abcline):
            foundtune = 1
            break
    if foundtune == 0:
        print("Tune '",tunename,"' Not found")
        return
#
#Output tune headers
    outfile.write(xline)
    outfile.write(abcline)
#
#Loop through the rest of the tune
    while 1:
        abcline = infile.readline()
        if not abcline: break
        abclineno = abclineno + 1
        if re.search("X:",abcline): break
        outfile.write(abcline)
#
#Finished with this tune
    return

# #Start point for script
main()

# All done.
