#!/bin/bash
export FLASK_APP=./src/main.py
pip3 install --user -r ./deps.txt
python3 -m flask run
