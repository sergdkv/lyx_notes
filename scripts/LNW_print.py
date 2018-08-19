#!/usr/bin/python

gcc_pattern="^(?P<filename>[^:]*):(?P<line>[0-9]*):(?P<col>[0-9]*): (?P<message>.*)"
bash_pattern="^(?P<filename>.*?): line (?P<line>[0-9]*): (?P<message>.*)"
pycompile_pattern=r"^[A-Za-z]*: [A-Za-z]*: \('(?P<message>[^']*)', \('(?P<filename>[^']*)', (?P<line>[0-9]*), (?P<col>[0-9]*), '(?P<err_line>[^']*)'\)\)\s*";

import sys
import re
import os
import json
import pprint

    
def CPPline_to_NWline( filename, line ):
    def nw_sort(x, y ):
        if x['line'] < y['line'] : return -1
        if x['line'] > y['line'] : return 1
        if x['col'] < y['col'] : return -1
        if x['col'] > y['col'] : return 1
        return 0
    index_fname = filename + '.nwindex'
    if os.path.exists( index_fname ):
        nwindex = json.load( file(index_fname) )
    else :
        return False

    target = { 'line': line, 'col': 0 }
    
    nwindex.sort( nw_sort )
    for n in nwindex:
       if nw_sort( n, target ) <= 0 :
            chank = n 
        
    nwfile = chank['nwfile']
    nwline = chank['nwline']  + (line - chank['line'])
    file_lines = file( filename ).readlines()

    l0 = max(0,line-3)
    #print line
    if line == len(file_lines) : line = len(file_lines) - 1
    #pprint.pprint( file_lines )
    lines_before = file_lines[ l0: line ]
    error_line = file_lines[ line ]
    lines_after = file_lines[ line+1: line +4 ]
    return { 
         'cppfile': filename,
         'nwfile': nwfile, 'nwline': nwline, 
         'error_line': error_line, 'lines_before': lines_before, 'lines_after': lines_after 
           }

a=sys.argv[1]
nlines = len(file(a).readlines())

for i in range(nlines):
    b = CPPline_to_NWline( a, i + 1)
    nwfile = b['nwfile']
    nwline = b['nwline']
    print i+1, nwline, file(nwfile).readlines()[nwline-1].rstrip(), " $$$ ", file(a).readlines()[i].rstrip()
    
