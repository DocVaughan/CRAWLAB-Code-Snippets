#! /usr/bin/env bash
#
# requires pdftops (part of the popler package)
# recommended install via homebrew via  >brew install poppler
#
# example use to convert all pdfs in the current directory to eps
#    prompt> pdfTOeps *.pdf 


for f in "$@" 
do
printf "Converting $f ... \n"
pdftops -eps "$f"
done