#!/usr/bin/python

import sys
import re
import json
import os
import pprint 

STARTHEAD="NWHEADSTART"
ENDHEAD="NWHEADEND"

cpp_text = sys.stdin.readlines()

cpp_line=0
cpp_index=[]
for line in cpp_text:
    cpp_line+=1
    pattern = STARTHEAD + "\s*line\s\s*([0-9]*)\s\s*file\s\s*\"(.*?)\"\s\s*" + ENDHEAD
    r=re.search( pattern, line )
    while True :
        r=re.search( pattern, line )
        if not r : break
        nw_file= os.path.basename( r.group(2) )
        nw_line= int(r.group(1))
        cpp_col= int(r.start(0))
        cpp_index  += [ { "nwline": nw_line, "line": cpp_line, "col": cpp_col, "nwfile": nw_file } ]
        line = line[:r.start(0)] + line[r.end(0):]

dump = json.dumps(cpp_index, sort_keys=True, indent=4 )
sys.stdout.write( dump )

