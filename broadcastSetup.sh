#!/bin/bash

cmd=~/groupDiv/setupNetworkProject.sh
listHost="S046V2pc02 S046V2pc04 S046V2pc06 S046V2pc07 S046V2pc09 S046V2pc11 S046V2pc13 S046V2pc15"

for host in $listHost;do
	ssh L15060101@$host $cmd
done
