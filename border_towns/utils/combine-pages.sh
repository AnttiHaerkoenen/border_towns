#!/bin/sh

FOLDER=$1
OUTPUT=$2
echo "${FOLDER} ${OUTPUT}"
FILES=${FOLDER}/*.txt
touch "${OUTPUT}"
for file in $FILES
do
    echo "Reading ${file}"
    echo "
---------------" >> $OUTPUT
    basename -s .txt $file >> $OUTPUT
    echo "---------------
" >> $OUTPUT
    cat $file >> $OUTPUT
done
echo "Complete."