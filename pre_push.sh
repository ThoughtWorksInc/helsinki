#!/bin/bash

pip install -r requirements.txt
nosetests
pep8 .
