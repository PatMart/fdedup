#!/bin/bash

PACKAGE=fdedup

if ! type virtualenv &>/dev/null; then
  echo "ERROR: can't find virtualenv. Have you installed it?"
  exit 1
fi

virtualenv venv

. ./venv/bin/activate

pip install -r test-requirements.txt
nosetests -v --with-xunit --all-modules --traverse-namespace --cover-xml \
        --with-xcoverage  --cover-package=$PACKAGE --cover-inclusive --cover-erase
coverage html
