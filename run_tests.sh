#!/bin/bash

PACKAGE=fdedup

if ! type virtualenv &>/dev/null; then
  echo "ERROR: can't find virtualenv. Have you installed it?"
  exit 1
fi

echo "Setting up virtualenv ..."
virtualenv -q venv2

echo "Activating virtualenv ..."
. ./venv/bin/activate

echo "Installing requirements ..."
pip install -q tox

echo "Running unittests ..."
tox