#!/bin/sh

PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH
if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate

pip install -r requirements.txt --download-cache=/tmp/$JOB_NAME
nosetests -v --with-xunit --all-modules --traverse-namespace --cover-xml --with-xcoverage  --cover-package=fdedup --cover-inclusive --cover-erase

if [ -d "venv" ]; then
        rm -rf venv
fi

