#!/usr/bin/env bash

export PYTHONPATH=${PYTHONPATH}:./src
export PYTHONPATH=${PYTHONPATH}:./test
echo $PYTHONPATH
pytest
