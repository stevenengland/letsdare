#!/bin/bash

if [[ "$VIRTUAL_ENV" != "" ]]
then
    echo "Active venv session detected. Please call 'deacticate' first."
    exit 1
fi

BASEDIR="$(readlink -f $0 | xargs dirname)/.."
echo ">> Deleting old virtual environment folder"
rm -rf $BASEDIR/.venv
echo ">> Creating new virtual environment folder"
python3 -m venv $BASEDIR/.venv
echo ">> Install dependencies"
source $BASEDIR/.venv/bin/activate
pip install -r ./requirements/dev.txt
echo ">> Done"