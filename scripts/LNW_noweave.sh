#!/bin/bash

INPUT="$1"
OUTPUT="$2"
ERROR=${INPUT}.noweave.errors

noweave -x -delay  "$INPUT" > "$OUTPUT" 2>"$ERROR"

cat $ERROR