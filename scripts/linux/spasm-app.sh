#!/bin/bash

if ! [ -r "$1" ]; then
	echo "Error: File could not be opened"
	exit
fi

echo -e "\e[1;33m# Starting SPASM TI83+ APP build script...\e[0m"

dir="$(cd "$( dirname "$0" )" && pwd)"

if [ "$(uname -o)" = "Cygwin" ]; then
	Platform="win"
else
	Platform="linux"
fi

if [ "$(uname -m)" = "x86_64" ]; then
	Bit="64"
else
	Bit="32"
fi

Compiler="$dir/../../funk/spasm/spasm-${Platform}${Bit}"

"$Compiler" "$1" "${1%.*}.8xk"
