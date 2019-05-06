#!/bin/zsh
WEBROOT=yes
if [ ! -d /webroot ]; then WEBROOT=no; fi

RUN=$(/usr/local/bigwebsite/start.sh)

if [ -d /webroot -a $WEBROOT = 'no' ]
then
	echo "folder /webroot created.\nif you are on a production server, move it to your virtual drive.\nthis folder should be accessed by a web server such as nginx to deploy relevant files.\nmodify the location of contents in these relevant scripts: start.sh production.ini"
fi

if [ -z "$RUN" ]
then
	echo 'start.sh returns zero length string'
	exit 1
fi

if [ "$RUN" = 'yes' ]
then
	~/bws.env/bin/pserve /usr/local/bigwebsite/development.ini --reload
fi
