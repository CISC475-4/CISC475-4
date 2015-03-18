#!/bin/bash

# Make sure the following packages are installed for this to work
# python-coverage
# python-nose
# python-mock

# For nose to find the unit tests, the filename of tests should start with Test.  
# The class name should also start with Test

# This will make a directory called cover with the generated html files
nosetests --with-coverage --cover-package a --cover-html