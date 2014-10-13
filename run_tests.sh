#!/bin/sh

PATH="$WORKSPACE/venv/bin:/usr/local/bin:$PATH"

rm -rf venv
virtualenv venv

. venv/bin/activate

pip install -r test-requirements.txt
nosetests -v --with-xunit --all-modules --traverse-namespace --cover-xml \
        --with-xcoverage  --cover-package=fdedup --cover-inclusive --cover-erase
coverage html

