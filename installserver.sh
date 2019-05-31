#!/bin/zsh

set -e -u

deleteafter=1
questionskip=1
developer=1

while getopts 'qdD' arg; do
	case "${arg}" in
		q) questionskip=0 ;;
		d) deleteafter=0 ;;
		D) developer=0 ;;
		*) echo "Invalid argument '${arg}'" ;;
	esac
done

function question
{
	if [ $questionskip -eq 1 ]
	then
		while true
		do
			printf "y/n: "
			read userin
			if [ $userin = 'y' ]
			then
				break
			elif [ $userin = 'n' ]
			then
				echo 'aborting'
				exit 0
			else
				echo "expected y or n --- you typed: $userin"
			fi
		done
	fi
	return 0
}

whoami > /dev/null; if [ $? -ne 0 ]
then
	if [ -z $USER ]
	then
		echo 'whoami failed and no $USER environment variable. exiting.'
		exit 1
	fi
	activeuser=$USER
else
	activeuser=$(whoami)
fi

dirname $0 > /dev/null; if [ $? -eq 0 ]
then
	pwd > /dev/null; if [ $? -ne 0 ]
	then
		if [ -z $PWD ]
		then
			echo 'pwd failed and no $PWD environment variable. exiting.'
			exit 2
		fi
		activedir="$( cd "$( dirname $0 )" > /dev/null && echo $PWD)"
	else
		activedir="$( cd "$( dirname $0 )" > /dev/null && pwd )"
	fi
else
	echo 'dirname $0 failed. exiting.'
	exit 3
fi

if [ -z $HOME ]
then
	echo 'no $HOME environment variable. exiting.'
	exit 3
fi

(python3 --version > /dev/null)
if [ $? -ne 0 ]
then
	echo 'python3 --version failed? exiting.'
	exit 4
fi

if [ $activeuser = 'root' ]
then
	echo 'installing as root. continue?'
	question
fi

if [ -d /usr/local/bigwebsite ]
then
	echo '/usr/local/bigwebsite exists. are you 100% positive you want to delete this and reinstall the server?'
	question
	rm -r /usr/local/bigwebsite
fi

if [ ! -d /usr/local/bigwebsite ]
then
	cp -r $activedir /usr/local/bigwebsite
	if [ ! -d ~/bigwebsite ]
	then
		ln -s /usr/local/bigwebsite ~/bigwebsite; if [ $? -ne 0 ]
		then
			echo 'failed to link /usr/local/bigwebsite to ~/bigwebsite'
		fi
	fi
fi

cd /usr/local/bigwebsite; if [ $? -ne 0 ]
then
	echo 'changing directory to /usr/local/bigwebsite failed. exiting.'
	exit 1
fi

if [ -d /usr/local/bigwebsite ]
then
	rm -r /usr/local/bigwebsite
fi

if [ ! -d /usr/local/bigwebsite ]
then
	cp -r $activedir /usr/local/bigwebsite
	if [ ! -d ~/bigwebsite ]
	then
		ln -s /usr/local/bigwebsite ~/bigwebsite; if [ $? -ne 0 ]
		then
			echo 'failed to link /usr/local/bigwebsite to ~/bigwebsite'
		fi
	fi
fi

cd /usr/local/bigwebsite; if [ $? -ne 0 ]
then
	echo 'changing directory to /usr/local/bigwebsite failed. exiting.'
	exit 1
fi

if [ -d ~/bws.env ]
then
	rm -rf ~/bws.env
fi

echo 'starting install process. please wait.'

python3 -m venv ~/bws.env > /dev/null
if [ $? -ne 0 ]
then
	tput setaf 1; echo '###############\n     ERROR\n###############'
	echo 'install failed at python3 -m venv ~/bws.env'
	exit 6
fi

chmod +x /usr/local/bigwebsite/bigwebsite.sh
if [ $? -ne 0 ]
then
	tput setaf 1; echo '###############\n     ERROR\n###############'
	echo 'install failed at chmod +x /usr/local/bigwebsite/bigwebsite.sh'
	exit 7
fi

if [ -h /usr/bin/bigwebsite ]
then
	rm /usr/bin/bigwebsite
fi

ln -s /usr/local/bigwebsite/bigwebsite.sh /usr/bin/bigwebsite
if [ $? -ne 0 ]
then
	tput setaf 1; echo '###############\n     ERROR\n###############'
	echo 'install failed at ln -s /usr/local/bigwebsite/bigwebsite.sh /usr/bin/bigwebsite'
	exit 8
fi

PIP=~/bws.env/bin/pip3
if [ ! -f $PIP ]
then
	PIP=~/bws.env/bin/pip
fi

if [ $developer -eq 0 ]
then
	$PIP install -e '.[dev]' > /dev/null
else
	$PIP install -e . > /dev/null
fi

if [ $? -eq 0 ]
then
	if [ $deleteafter -eq 0 ]
	then
		rm -rf ~/bigwebsite
	else
		echo 'install complete.\nto reinstall just run this file again.'
	fi
else
	tput setaf 1; echo '###############\n     ERROR\n###############'
	echo 'install failed at ~/bws.env/bin/pip install -e .'
	exit 9
fi

exit 0
