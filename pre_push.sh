#!/bin/bash

pip install -r requirements.txt
pip install -r requirements_for_tests.txt
nosetests && pep8 .
