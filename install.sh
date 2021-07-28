#!/usr/bin/env bash

ver=`/usr/bin/env python -c "from __future__ import print_function;import sys;print(sys.version[0])"`
if [ $? -ne 0 ];then
	echo "Could find any python installation."
	exit 1
fi
pyexe=`which python`
if [ $ver -ne 3 ]; then
	which python3 1>/dev/null 2>&1
	if [ $? -ne 0 ];then
		echo "Could not find any python3 installation."
		exit 1
	fi
	pyexe=`which python3`
fi

import_path=`python3 -c "import sys;print(sys.path[-1] + '/baton')"`
mkdir $import_path
cp -f __init__.py $import_path
if [ $? -ne 0 ];then
    echo "Unable to copy file(s) to "$import_path\
			 ". Try running the script as sudo e.g. > sudo ./install.sh"
	exit 1
fi

echo "baton installed in "$import_path

