#!/bin/bash
set -B

usage () {
	cat << EOF
./main.sh [options]

h: Shows this message.
i: Install requirements.
c: Allows account creation.
EOF
	exit $1
}

while getopts "hci" opt
do
	case $opt in
		h)
			usage 0
			;;
		c)
			export KEPT_FOLDER_AC=1
			;;
		i)
			pip3 install --user -r ./deps.txt
			exit
			;;
	esac
done

# Exports
export FLASK_APP=./src/main.py

# Init stuff
rm -rf test
mkdir -p {disk,test}/{users,log}
touch {disk,test}/log/{keys,log}

# Start
python3 -m flask run --host=0.0.0.0
