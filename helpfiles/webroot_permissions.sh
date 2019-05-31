#!/bin/bash
function fix
{ 
	for x in $1/*
	do 
		if [ -d $x -a ! -f $x ]
		then 
			chmod 755 $x
			fix $x
		else
			if [ -f $x -a -r $x ]
			then 
				chmod 644 $x
			fi
		fi
	done
}

fix $1
