#!/usr/bin/python

gcc_pattern="^(?P<filename>[^:]*):(?P<line>[0-9]*):(?P<col>[0-9]*): (?P<message>.*)"
bash_pattern="^(?P<filename>.*?): line (?P<line>[0-9]*): (?P<message>.*)"
pycompile_pattern=r"^[A-Za-z]*: [A-Za-z]*: \('message>[^']*)', \('(?P<filename>[^']*)', (?P<line>[0-9]*), (?P<col>[0-9]*), '(?P<err_line>[^']*)'\)\)\s*";
pycompile_pattern=r"^[A-Za-z]*:([ A-Za-z]*:)? \((?P<errdict>.*)\)\s*";
notangle_pattern="^(?P<filename>.*\.nw?):(?P<line>[0-9]*):(?P<col>) (?P<message>.*)"


import sys
import re
import os
import json
import pprint

def print_TeX_err_message( cppfilename, line, nwfilename, nwline, nwmessage, lines_before, error_line, lines_after ):
    print "! " + os.path.basename(cppfilename) + " :" + str(line)
    print "l." + str(nwline) + " "
    print nwmessage
    for l in lines_before: print '???', l.rstrip()
    for l in [error_line]: print '>>>', l.rstrip()
    for l in lines_after:  print '???', l.rstrip()
    
def CPPline_to_NWline( filename, line ):
    def nw_sort(x, y ):
        if x['line'] < y['line'] : return -1
        if x['line'] > y['line'] : return 1
        if x['col'] < y['col'] : return -1
        if x['col'] > y['col'] : return 1
        return 0
    a = os.path.basename(filename)
    b = os.path.dirname(filename)
    index_fname = os.path.join(b, '.' + a + '.nwindex' )
    
    nwindex = None
    if os.path.exists( index_fname ):
        nwindex = json.load( file(index_fname) )
    if nwindex is None :
        d = os.path.dirname( index_fname )
        b = os.path.basename( index_fname )
        a = d + '/.' + b
        if os.path.exists( a ):
            nwindex = json.load( file( a ) )
    if nwindex is None :
        print >>sys.stderr, "File " , index_fname , ' ' , a , " is not exist or is not json file"
        return False

    target = { 'line': line, 'col': 0 }
    
    nwindex.sort( nw_sort )
    for n in nwindex:
       if nw_sort( n, target ) <= 0 :
            chank = n 
        
    nwfile = chank['nwfile']
    nwline = chank['nwline'] + (line - chank['line'])
    # print >>sys.stderr, chank['nwline'], line, chank['line']
    file_lines = file( filename ).readlines()

    l0 = max(0,line-3)
    #print line
    if line > len(file_lines) : line = len(file_lines)
    #pprint.pprint( file_lines )
    lines_before = file_lines[ l0: line - 1 ]
    error_line = file_lines[ line  - 1]
    lines_after = file_lines[ line: line +3 ]
    return { 
         'cppfile': filename,
         'nwfile': nwfile, 'nwline': nwline, 
         'error_line': error_line, 'lines_before': lines_before, 'lines_after': lines_after 
           }

def NWline_to_NWline( filename, line ):
    nwline = line
    nwfile = filename

    file_lines = file( filename ).readlines()
    l0 = max(0,line-3)
    #print line
    if line > len(file_lines) : line = len(file_lines)
    #pprint.pprint( file_lines )
    lines_before = file_lines[ l0: line-1 ]
    error_line = file_lines[ line-1 ]
    lines_after = file_lines[ line: line +3 ]
    
    return { 
         'cppfile': filename,
         'nwfile': nwfile, 'nwline': nwline, 
         'error_line': error_line, 'lines_before': lines_before, 'lines_after': lines_after 
           }

### MAIN PROGRAM ###
for s in sys.stdin:
    error_parsed = False 
    for P in [ gcc_pattern, bash_pattern ] :
       res = re.match( P, s )
       if res :
          filename=res.group('filename')
          line= int(res.group('line'))
          message=res.group('message')
          error_parsed = True
          #print >>sys.stderr, P
       pass
    pass
    for P in [ pycompile_pattern ] :
       res = re.match( P, s )
       if res :
          b = eval( res.group('errdict') )
          message=b[0]
          filename=b[1][0]
          line= int( b[1][1] )
          error_parsed = True
          #print >>sys.stderr, 'message=', message, 'filename=', filename, 'line=',line
       pass
    pass

    if not error_parsed:
       res = re.match( notangle_pattern, s )
       if res :
          filename=res.group('filename')
          line= int(res.group('line'))
          message=res.group('message')
          error_parsed = True
          error_descr = NWline_to_NWline( filename, line )
    else :
       if error_parsed:
          #print >>sys.stderr, filename, line
          error_descr = CPPline_to_NWline( filename, line )
          if error_descr == False : error_parsed = True

    if not error_parsed :
        print s
        print >>sys.stderr, s
    elif error_parsed and error_descr == False :
        print "error_descr == False (LNW_parse_errors.py)"
        print s
        print >>sys.stderr, "error_descr == False (LNW_parse_errors.py)"
        print >>sys.stderr, s
    else :
        print
        print_TeX_err_message( 
                 error_descr['cppfile'], 
                 line, 
                 error_descr['nwfile'], 
                 error_descr['nwline'], 
                 message, 
                 error_descr['lines_before'], 
                 error_descr['error_line'], 
                 error_descr['lines_after'] )
        print
        pass
    pass
pass


