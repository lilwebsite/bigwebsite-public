#!/bin/zsh
RUN=no
whoami > /dev/null; if [ $? -ne 0 ]
then
	if [ $USER = '' ] 
	then
		echo 'whoami failed and no $USER environment variable. exiting.'
		exit 1
	fi
	activeuser=$USER
else
	activeuser=$(whoami)
fi

if [ -d /usr/local/bigwebsite ]
then
	cd /usr/local/bigwebsite
	if [ ! -d /webroot ]; then cp -r ./webroot /webroot; fi
	if [ ! -d ~/bws.env ]
	then
		echo 'python environment not set up. please run installserver.sh'
		exit 1
	fi
	RUN=yes
else
	echo "/usr/local/bigwebsite doesn't exist..."
	exit 1
fi

echo "$RUN"
exit 0
