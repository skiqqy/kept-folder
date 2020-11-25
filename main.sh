#!/bin/bash
set -B
export FLASK_APP=./src/main.py
rm -rf test
mkdir -p {disk,test}/{users,log}
touch {disk,test}/log/{keys,log}
pip3 install --user -r ./deps.txt
python3 -m flask run
