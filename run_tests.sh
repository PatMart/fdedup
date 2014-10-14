#!/bin/bash

PACKAGE=fdedup

if ! type virtualenv &>/dev/null; then
  echo "ERROR: can't find virtualenv. Have you installed it?"
  exit 1
fi

echo "Setting up virtualenv ..."
virtualenv -q venv

echo "Activating virtualenv ..."
. ./venv/bin/activate

echo "Installing requirements ..."
pip install -q -r test-requirements.txt

echo "Running unittests ..."
nosetests -v --with-xunit --all-modules --traverse-namespace --cover-xml \
        --with-xcoverage  --cover-package=$PACKAGE --cover-inclusive --cover-erase

echo "Generating coverage report ..."
coverage html
