#!/usr/bin/env python2

"""
Source code in FileUtility.py regards reading the data from a structured CSV file into memory

This accounts for the step between raw data and storage in the database
"""
#TODO: multithreading with python threading library

import xlrd
import sys
import datetime

from time import time
from re import sub


class Instance(object):
    """
    A data instances given data type headers and the corresponding values.
    Instances are stored in a dictionary (Instance.Data) where the headers are keys

    IE. an Instance is a single row in a spreadsheet with corresponding data header, for single key-value pairs
    """
    #TODO: add metadata for each related instance 


    """
    __init__ input: header is a list of headers
		                values is a list of values
    """
    def __init__(self, header=[], values=[]):
        self.Data = {}

        for i in range(0, len(header)):
            self.Data[header[i]] = values[i]

    def __repr__(self):
        return str(self.Data)


def get_data_from(path):

    """
    performs the simple tasks of reading in data instances.
    Returns a tuple of data instances and the corresponding column headers
    """

    columns = []     # the headers
    instances = []   # a set of Instances

    try:
        with open(str(path), 'r') as dataFile:
            columns = dataFile.readline().strip().split(',')
            for nextLine in dataFile: 
                d = nextLine.strip().split(',')
                n = Instance(columns, d)
                instances.append(n)
    except IOError:
        print >> sys.stderr, "Unable to open file at %s" % (path)

    return (columns, instances)


def xls_to_csv(path):
    """
    Convert all spreadsheets in file 'path' to a csv. Saved file is named w/ concatenation of path & spreadsheet name
    NOTE: input MUST be in '.xls' or '.xlsx' format

    Returns the pathname of each created file
    """
    names = [] #for return

    try:
        with xlrd.open_workbook(path) as wb:
            n = wb.nsheets #worksheets 
            # convert each sheet in wb to its own csv
            for i in range(0, n):
                doc = wb.sheet_by_index(i) #current worksheet
                r = doc.nrows #rows
 
                csv = open(sub('\.xls[x]$','',path) + doc.name + '.csv', 'w')
                names.append(str(csv.name)) #for return
            
                for j in range(0, r):
                    row_str = ""

                    for cell in doc.row_values(j):
                    #need to change the values from floats to match the original data
                        if type(cell) == float and cell % 1 == 0:
                            cell = int(cell)
                        row_str += str(cell) + ','

                    #remove trailing ',' and write
                    csv.write(row_str[0:len(row_str)-2] + '\n')
            
                wb.unload_sheet(i)
                csv.close()
    except IOError:
        print >> sys.stderr, "Unable to open file at %s" % (path)
        return 

    return tuple(names)
