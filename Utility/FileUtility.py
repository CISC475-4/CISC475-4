
"""
Source code in FileUtility.py regards reading the data from a structured CSV file into memory

This accounts for the step between raw data and storage in the database
"""

import xlrd

from re import sub

class Instance(object):
 
    """
    A data instances given data type headers and the corresponding values. 
    Instances are stored in a dictionary (Instance.Data) where the headers are keys
    """

    def __init__(self, header=[], values=[]):
        self.Data = {}
        for i in range(0,len(header)): 
            self.Data[header[i]] = values[i]

    def __repr__(self):
        return str(self.Data)



def getDataFrom(path):

    """
    performs the simple tasks of reading in data instances. 
    Returns a tuple of data instances and the corresponding column headers 
    """

    columns = []     # the headers
    instances = []   # a set of Instances

    with open(str(path), 'r') as dataFile:
        columns = dataFile.readline().strip().split(',')
        for nextLine in dataFile: 
            d = nextLine.strip().split(',')
            n = Instance(columns, d)
            instances.append(n)

    return (columns, instances)


def XLStoCSV(path):
    """
    Convert all spreadsheets in file 'path' to a csv. Saved file is named w/ concatenation of path & spreadsheet name
    NOTE: input MUST be in '.xls' or '.xlsx' format
    """

    with xlrd.open_workbook(path) as wb:
        n = wb.nsheets #worksheets
        # convert each sheet in wb to its own csv
        for i in range(0, n):
            doc = wb.sheet_by_index(i) #current worksheet
            r = doc.nrows #rows
 
            csv = open(sub('\.xls[x]$','',path) + doc.name + '.csv', 'w')
            
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
