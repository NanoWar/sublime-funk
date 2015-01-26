#!/bin/bash

if ! [ -r "$1" ]; then
	echo "Error: File could not be opened"
	exit
fi

dir="$(cd "$( dirname "$0" )" && pwd)"

if ! [ -n "$2" ]; then
	sh "$dir/../../funk/build.sh" "$1"
else
	# Goto sublime project directory and look for configuration there...
	if [ -r "$2/funk.config" ]; then
		cd $2
		sh "$dir/../../funk/build.sh" "$1"
	else
		sh "$dir/../../funk/build.sh" "$1"
	fi
fi
