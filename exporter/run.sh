#!/bin/sh

echo "Download examples from repo"
wget https://github.com/hadar-simulator/hadar/archive/master.zip
unzip master.zip
mv hadar-master/examples examples
rm -r hadar-master
rm master.zip

echo "Setup python env"
python3 -m virtualenv venv
source venv/bin/activate
pip install -r examples/requirements.txt

echo "Launch exporter"
python3 exporter.py

echo "clean"
rm -r venv
rm -r examples

