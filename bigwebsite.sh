#!/bin/zsh
WEBROOT=yes
BWS=/usr/local/bigwebsite
if [ ! -d /webroot ]; then WEBROOT=no; fi

RUN=$($BWS/start.sh)

if [ ! -f $BWS/data.sqlite -a ! -f /webroot/data.sqlite ]
then
	echo "first time startup, set up users"
	$BWS/init_db.sh
fi

if [ -d /webroot -a $WEBROOT = 'no' ]
then
	echo
	echo "folder /webroot created.\nif you are on a production server, move it to your virtual drive.\nthis folder should be accessed by a web server such as nginx to deploy relevant files.\nmodify the location of contents in these relevant scripts: start.sh production.ini"
	echo
fi

if [ -z "$RUN" ]
then
	echo 'start.sh returns zero length string'
	exit 1
fi

if [ "$RUN" = 'yes' ]
then
	~/bws.env/bin/pserve $BWS/development.ini --reload
fi
