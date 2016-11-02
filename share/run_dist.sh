#!/usr/bin/env bash

DIR=$(cd "$(dirname "$0")"; pwd)
cd $DIR
python rsc/resourcer.py Resourcer
# ./rsc/resourcer.py
