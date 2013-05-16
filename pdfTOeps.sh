#! /usr/bin/env bash

# example use to convert all pdfs in the current directory to eps
#    prompt> pdfTOeps *.pdf 


for f in "$@" 
do
printf "Converting $f ... \n"
pdf2ps "$f"
eps2eps "${f%.*}.ps" "${f%.*}.eps"
rm *.ps 
done