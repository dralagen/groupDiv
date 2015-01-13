#!/bin/bash
# scenario.sh
# Scenario to test groupDiv: two users diva1 and diva2
# diva2 clone diva1 
# Configuration

#Put your own directory

DIR='/tmp' 
DIVA1='diva1'
DIVA2='diva2'

FDIVA1='diva1.txt'
FDIVA2='diva2.txt'


# Each repository must have different files (diva1.txt written by diva1 and diva2.txt written by diva2)
# Each repostory must have a comments file (diva1Comment.txt,
# Action diva1 
 
echo "--"
echo "-- update diva1:"
echo "-- $DIR/$DIVA1"
echo "--"

cd $DIR'/'$DIVA1
echo 'diva1' >> diva1.txt 
git commit -am "second diva1 commit"

echo "--"

sleep 5

# Action diva2 

echo "--"
echo "-- diva2 pull from diva1:"
echo "-- $DIR/$DIVA2"
echo "--"


cd $DIR'/'$DIVA2

git pull

sleep 5

# Action diva1 
 
echo "--"
echo "-- update diva1:"
echo "-- $DIR/$DIVA1"
echo "--"

cd $DIR'/'$DIVA1
echo 'diva1' >> diva1.txt 
git commit -am "second diva1 commit"

echo "--"

sleep 5

# Action diva2

echo "--"
echo "-- update diva2:"
echo "-- $DIR/$DIVA2"
echo "--"

cd $DIR'/'$DIVA2
echo 'diva2' >> diva1.txt
git commit -am "second diva2 commit"

echo "--"

sleep 5

# Action diva1 
 
echo "--"
echo "-- update diva1:"
echo "-- $DIR/$DIVA1"
echo "--"

cd $DIR'/'$DIVA1
echo 'diva1' >> diva2.txt
git pull $DIR/$DIVA2

sleep 5

# Action diva1 
 
echo "--"
echo "-- update diva1:"
echo "-- $DIR/$DIVA1"
echo "--"

cd $DIR'/'$DIVA1
echo 'diva1' >> diva1.txt 
git commit -am "second diva1 commit"

echo "--"

sleep 5

# Action diva2 

echo "--"
echo "-- diva2 pull from diva1:"
echo "-- $DIR/$DIVA2"
echo "--"


cd $DIR'/'$DIVA2

git pull

sleep 5
