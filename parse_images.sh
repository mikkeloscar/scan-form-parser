#!/bin/bash

# remove images in billeder
echo "Cleaning 'billeder'-folder"
rm billeder/*.jpg

infile=$1
outfile="tmp.png"

echo "Converting pdf to pngs"

convert -density 300x300 -quality 100 $infile $outfile

for file in tmp*.png; do
    python3 parse_image.py $file billeder
done

# cleanup
rm tmp*.png
