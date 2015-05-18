#!/usr/bin/env python2

"""Sets up the package information and installs 

To create a new source distribution:
    $ /usr/bin/env python2 setup.py sdist

This file can also install the package to system-wide directories on the user's
computer, but currently that would be a bad idea because every py_modules item
will be installed as its own module, which isn't what we want. A simple fix to
this would be to create a folder containing all of the files in the current
project directory and give it its own __init__.py. The setup.py script can be 
placed in the same directory as the new folder. If the install is done with
that directory structure, our product will be taken as a single package, and it
will be installed accordingly.

To install globally:
    # /usr/bin/env python2 setup.py install
"""

from distutils.core import setup

setup(
    name = 'CISC475 Data Visualization',
    version = '1.0.0',   
    description = 'Graph research data of a specified format to facilitate ' +
        'visualizing changes in the data',
    long_description = open('README.txt').read(),
    author = 'Matt Hoffman, Ryan Keeley, Jamie Luck, Kelly Peterson, ' +
        'Brandon Trautmann, Andrew Shearer',
    author_email = 'mhoffman@udel.edu, rkeeley@udel.edu, jluck@udel.edu, ' +
        'keldryc@udel.edu, btraut@udel.edu, aishear@udel.edu',
    url = 'https://github.com/CISC475-4/CISC475-4',
    # What we want our package to be called. Folder name needs to be that, too.
    #package = ['dataviz']
    package_dir = { 'dataviz' : '.' },
    # Pure Python modules
    py_modules = [ # prepend these with dataviz/ if I move the stuff over
        'main',
        'controller.database',
        'controller.controller',
        'ui.mainui',
        'ui.vizdialog',
        'ui.vizgraphing',
        'ui.vizmenubar',
        'ui.viztoolbar',
        'utility.file_utility'
    ],
    # Non-code files the package requires
    package_data = { 'dataviz' : ['ui/ui_assets/*.png', 
        'controller/schemata/main.sql', 'run'] },
    data_files = [
        ('graphics', ['ui/ui_assets/*.png']),
        ('databases', ['controller/schemata/main.sql'])
    ]#,
    # Extra files that aren't necessary to the program's execution
    #data_files = [...]
)

"""    modules = [
        'matplotlib',
        'numpy',
        'PySide'
        'xlrd',
    ],
"""
