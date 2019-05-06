#!/bin/zsh
BWS=/usr/local/bigwebsite
RUN=$($BWS/start.sh)
if [ -z "$RUN" ]
then
	echo 'start.sh returns zero length string'
	exit 1
fi
if [ "$RUN" = 'yes' ]
then
	~/bws.env/bin/pytest $BWS/unit-tests/tests.py
else
	echo "$RUN"
fi
