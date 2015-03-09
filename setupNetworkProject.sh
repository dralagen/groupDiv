#!/bin/bash
# ./setupNetworkProject.sh
# by Dralagen
#
# Create a repo and launch a git daemon for share it
#
# Warning this script kill git-daemon if already launched
#

if [ -z "$DIVA_REPO_DIR" ]; then
	echo "Error set env \$DIVA_REPO_DIR with : export DIVA_REPO_DIR=\"/tmp/diva/\""
	exit 1
fi

#
# Clean older repository
#
if [ -d "$DIVA_REPO_DIR" ]; then
    echo "--"
    echo "-- Clean repo"
    echo "--"

    # kill git-daemon
    GIT_DAEMON_PID=`ps -C git-daemon -o pid= \
     || ps -ef | grep git-daemon | grep -v grep | awk "{print \$2}"`

    if [ -n "$GIT_DAEMON_PID" ]; then
        kill -9 $GIT_DAEMON_PID 2>/dev/null && echo "kill git-daemon"
    fi

    rm -rf "$DIVA_REPO_DIR" && echo "remove $DIVA_REPO_DIR"

    echo "--"
fi

#
# Create Repo
#
echo "--"
echo "-- Create repo at : "
echo "-- $DIVA_REPO_DIR"
echo "--"

mkdir -p "$DIVA_REPO_DIR" && cd $_ && git init

echo "--"


#
# Launch git daemon
#

echo "--"
echo "-- launch git daemon"
echo "--"

git daemon --base-path="$DIVA_REPO_DIR" --detach --export-all && echo "git-daemon launched"

echo "can pull on git://`hostname`/"

echo "--"

