#!/bin/sh

echo "Download examples from repo"
wget https://github.com/hadar-simulator/hadar/archive/master.zip
unzip master.zip
rm master.zip
mv hadar-master/examples examples
rm -r hadar-master

echo "Setup python env"
python3 -m virtualenv venv
source venv/bin/activate
pip install -r examples/requirements.txt
pip install click

echo "Launch exporter"
python3 utils.py --src=./examples --export=../assets/notebook

echo "clean"
rm -r venv
rm -r examples

