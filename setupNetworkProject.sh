#!/bin/bash
# ./setupNetworkProject.sh
#
# Create a repo and launch a git daemon for share it
#
# Warning this script kill git-daemon if already launched
#

REPO_DIR="/tmp/diva/"

#
# Clean older repository
#
if [ -d "$REPO_DIR" ]; then
    echo "--"
    echo "-- Clean repo"
    echo "--"

    # kill git-daemon
    GIT_DAEMON_PID=`ps -C git-daemon -o pid= \
     || ps -ef | grep git-daemon | grep -v grep | awk "{print \$2}"`

    if [ -n "$GIT_DAEMON_PID" ]; then
        kill -9 $GIT_DAEMON_PID 2>/dev/null && echo "kill git-daemon"
    fi

    rm -rf "$REPO_DIR" && echo "remove $REPO_DIR"

    echo "--"
fi

#
# Create Repo
#
echo "--"
echo "-- Create repo at : "
echo "-- $REPO_DIR"
echo "--"

mkdir -p "$REPO_DIR" && cd $_ && git init

echo "--"


#
# Launch git daemon
#

echo "--"
echo "-- launch git daemon"
echo "--"

git daemon --base-path="$REPO_DIR" --detach --export-all && echo "git-daemon launched"

# TODO check if hostname work in network else use ip
echo "can pull on git://`hostname`/"

echo "--"

