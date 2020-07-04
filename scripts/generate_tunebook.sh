#!/bin/bash
abcm2ps -O pgh_session_tunebook_raw.ps -F pgh_session_tunebook.fmt ^
andy_cutting_tunes.abc
#pause 'hit return'
tclsh abcmaddidx.tcl pgh_session_tunebook_raw.ps pgh_session_tunebook.ps
#pause 'hit return'
rm pgh_session_tunebook_raw.ps
