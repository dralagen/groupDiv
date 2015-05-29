#!/bin/bash

if [ $# -eq 1 ] ; then
	log="$1"
fi

GDtotLog="`cat "$log" | grep "INFO:"`"
delta=0
echo "$GDtotLog" | while read l ; do
	line="`echo "$l" | grep "GDtot"`"
	if [[ -n $line ]] ; then
		delta="`echo $line | grep -o "delta=[0-9]*" | awk -F"=" '{print $2}'`"
	else
		line="`echo "$l" | grep "commit"`"
		if [[ -n $line ]] ; then
			echo "`echo $line | awk -F':' '{print $5}'`" ";" $delta
		fi
	fi
			
done
