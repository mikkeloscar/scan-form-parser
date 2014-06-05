#!/bin/sh

BASE=/tmp/tesseracttemp_$$
PIPE=$BASE.txt

rm -f      $PIPE
mkfifo     $PIPE
tesseract  "$@" $BASE digits 1>/dev/null 2>&1 &
cat        $PIPE
rm -f      $PIPE
