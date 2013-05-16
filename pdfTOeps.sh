#! /usr/bin/env bash

for f in "$@" 
do
printf "Converting $f ... \n"
pdf2ps "$f"
eps2eps "${f%.*}.ps" "${f%.*}.eps"
rm *.ps 
done