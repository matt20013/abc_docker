#!/usr/bin/env tclsh

# Create a tune index from the abcm2ps XHTML output
#	
# Copyright (C) 2013 Jean-François Moine
# version 2013/11/02
#	- add links to the pages in the index
# version 2013/11/01
#	- first version - use with abcm2ps >= 7.6.4
#
# Know bugs:
#	- Tcl encodes the utf-8 characters into utf-16 so that the
#	  musical characters (range 0x1d100 .. 0x1d1ff) are lost.

# -- set your preferences here --
	set style {style="font-family:Times; font-size:18px;"}
#	set style {}
	set table-width {70%}
# -- end preferences --

proc usage {} {
    puts {Add a tune index to a abcm2ps XHTML output.
Usage: ./abcmaddidx2.tcl [options] <input abcm2ps file> <output file with index>
  <input abcm2ps file> may be '-' for stdin
  -b     set the index before the music}
	exit 1
}

proc main {} {
    global argv style table-width
    set fnin {}
    set fnout {}
    set before 0
    foreach p $argv {
	switch -- $p {
	    -b {
		set before 1
	    }
	    default {
		if {[string length $fnin] == 0} {
		    set fnin $p
		} elseif {[string length $fnout] == 0} {
		    set fnout $p
		} else {
			usage
		}
	    }
	}
    }
    if {$fnin == "-"} {
	set in stdin
    } else {
	set in [open $fnin r]
    }
    set out [open $fnout w]
    set titlelist {}
    set gsave {}
    set scale {}
    set margin {}

    # copy the header
    while {[gets $in line] >= 0} {
	puts $out $line
	if {[string compare $line {<body>}] == 0} {
	    break
	}
    }
    if {$before} {
	set before [tell $in]
    }
    set page 0
    while {[gets $in line] >= 0} {
	switch [string range $line 0 4] {
	    {<svg } {
		incr page
		set line [string replace $line 4 4 " id=\"page$page\" "]
	    }
	    {<!-- } {
		if {[string compare [string range $line 5 10] {title:}] == 0} {
		    set title [string range $line 12 end-4]
		    lappend titlelist \
[list $title "<td><a href=\"#page$page\">$title</a></td><td>$page</td>"]
		} elseif {[string compare [string range $line 5 13] {subtitle:}] == 0} {
		    set title [string range $line 15 end-4]
		    lappend titlelist \
[list $title "<td><a href=\"#page$page\">$title</a></td><td>$page</td>"]
		}
	    }
	    </bod {
		 break
	    }
	}
	if {!$before} {
	    puts $out $line
	}
    }
    # output the index
    puts $out "<div align=\"center\" $style>
<h2>Index</h2>
<table width=\"${table-width}\">"
	foreach t [lsort -index 0 $titlelist] {
	    puts $out "<tr>[lindex $t 1]</tr>"
	}
    puts $out {</table>
</div>}

    # if index at the beginning, copy the body
    if {$before} {
	seek $in $before
	set page 0
	while {[gets $in line] >= 0} {
		switch [string range $line 0 4] {
		    {<svg } {
			incr page
			set line [string replace $line 4 4 " id=\"page$page\" "]
		    }
		    </bod {
			 break
		    }
		}
		puts $out $line
	}
    }
    puts $out {</body>
</html>}
}

# -- main
if {$argc < 2} {
    usage
}

main
