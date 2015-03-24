#!/bin/bash

if [ $# -eq 1 ] ; then
	log="$1"
fi

GDtotLog="`cat "$log" | grep "INFO:" | grep "GDtot"`"

GDtotField="`echo "$GDtotLog" | head -n1`"
GDtotField="`echo "$GDtotField" | awk -F':' '{print $5}' | tr ';' ' '`"
field="datetime"
for f in $GDtotField; do
	field=$field",`echo "$f" | awk -F'=' '{print $1}'`"
done
echo $field
echo "$GDtotLog" | while read l ; do
	field="`echo "$l" | awk -F':' '{print $2":"$3":"$4}' | awk -F',' '{print $1}'`"
	divaInfo="`echo "$l" | awk -F':' '{print $5}' | tr ';' ' '`"
	for f in $divaInfo; do
		field=$field",`echo $f | awk -F'=' '{print $2}'`"
	done
	echo $field
done
