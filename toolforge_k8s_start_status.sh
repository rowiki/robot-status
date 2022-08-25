#!/bin/bash

set -x

python3 -m pip install --upgrade pip "setuptools>=49.4.0, !=50.0.0, <50.2.0" wheel requests kubernetes

cd /data/project/patrocle/robot-status
export PYTHONPATH=/data/project/.shared/pywikibot/core_stable:$PYTHOPATH
python3 main.py
