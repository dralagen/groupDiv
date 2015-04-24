#!/bin/bash

if [ $# -eq 1 ] ; then
	log="$1"
fi

echo "user;nbPull;alreadyUpToDay;nbCommitUE;nbCommitReview"

i=1;
for f in $log/*.log; do
	#echo $f;
	echo "usr$i;"\
		"`cat $f | grep "pull" | wc -l`;"\
		"`cat $f | grep "pull" | grep "Already up-to-date" | wc -l`;"\
		"`cat $f | grep ":commit update ue" | wc -l`;"\
		"`cat $f | grep ":commit new review" | wc -l`";
	i=$(($i+1))
done

