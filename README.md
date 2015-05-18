# CISC475-4
This is the repository for group 4 of the University of Delaware's Spring 2015 
Advanced Software Engineering class, working on a data vision project.

Our project parses datasets into an embedded sqlite database, then does 
transformations on the data before rendering it interactively using matplotlib 
inside of a PySide QT GUI. The whole project is written in Python.

For more information, consult the documentation and comments in the source code.

## Usage

Start the program    
```
$ /usr/bin/env python2 main.py
```    
or    
```
$ ./run
```

Run tests    
```
$ nosetests --exe
```    
or    
```
$ /usr/bin/env python2 -m unittest test.test_database
```

Generate code coverage reports    
```
$ nosetests --exe --with-coverage --cover-tests
```    
You can also write the results to an HTML file that can be viewed on your
computer. Create or find a directory into which you want the HTML files to be
placed. Let that directory be called `$HTML`.    
```
$ nosetests --exe --with-coverage --cover-tests --cover-html \
  --cover-html-dir=$HTML
```    
After that command has been run, you can open up your favorite Internet
browser, press <kbd>&#8984;</kbd> + <kbd>o</kbd> or go to File > Open, switch
to `$HTML`, and select the report you want to view.

Generate documentation, for example, of the test/test\_database.py file. The
`-w` flag is optional, and causes pydoc to write its generated documentation to
the current directory.
```
$ /usr/bin/env python2 -m pydoc test.test_database
```    
