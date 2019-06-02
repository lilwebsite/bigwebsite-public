#!/bin/bash

ini_file=development.ini

_usage ()
{
	echo "usage ${0} [options]"
	echo
	echo "initialized the database, will initialize to the install directory if no options provided."
	echo "if the option -P is given, it will use the production.ini file."
	echo
	echo "-P		Use production.ini settings"
	echo "			 Default: ${ini_file} settings"
	echo "-D		Use test.ini settings"
	echo "			 Default: ${ini_file} settings"
	echo "-h		This help message"
	exit ${1}
}

while getopts 'PDh' arg; do
	case "${arg}" in
		P) ini_file=production.ini ;;
		D) ini_file=test.ini ;;
		h) _usage 0 ;;
		*)
			echo "Invalid argument ${arg}"
			_usage 1 ;;
	esac
done

systemctl stop bigwebsite
~/bws.env/bin/initialize_bigwebsite_db /usr/local/bigwebsite/$ini_file
