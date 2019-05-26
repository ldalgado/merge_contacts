#!/usr/bin/env bash
cd $(dirname "$0")
export PYTHONPATH=${PYTHONPATH}:./src
export PYTHONPATH=${PYTHONPATH}:./test
echo $PYTHONPATH
python src/merge_contacts.py
