#!/bin/bash

cmd=~/groupDiv/setupNetworkProject.sh
listHost="S046V2pc07 S046V2pc08 S046V2pc09 S046V2pc10 S046V2pc11 S046V2pc12 S046V2pc13 S046V2pc14"

for host in $listHost;do
	ssh L15060101@$host $cmd
done
