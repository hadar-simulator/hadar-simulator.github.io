#!/bin/sh

echo "Download examples from repo"
git clone https://github.com/hadar-simulator/hadar
git lfs pull
mv hadar/examples examples
rm -rf hadar

echo "Setup python env"
python3 -m virtualenv venv
source venv/bin/activate
pip install -r examples/requirements.txt
pip install click

echo "Launch exporter"
python3 examples/utils.py --src=./examples --export=./assets/notebook

echo "clean"
rm -r venv
rm -r examples

