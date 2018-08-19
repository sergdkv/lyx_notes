#!/bin/bash


ERROR=`ls *.noweave.errors | head -n1`
if [ -z "$ERROR" ] ; then exit 0; fi;

cat $ERROR | awk "match( \$0, /(.*\.nw):([0-9]*):(.*)/, a) {print \"\"; print \"! \" a[1] \" \"   \"\nl.\" a[2] \" \" a[3] ; print \"noweave error\"; next; }{print \$0}"



