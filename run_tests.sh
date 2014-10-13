#!/bin/sh

PACKAGE=fdedup

virtualenv venv

. ./venv/bin/activate

pip install -r test-requirements.txt
nosetests -v --with-xunit --all-modules --traverse-namespace --cover-xml \
        --with-xcoverage  --cover-package=$PACKAGE --cover-inclusive --cover-erase
coverage html

