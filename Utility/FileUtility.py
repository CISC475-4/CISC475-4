
"""
Source code in FileUtility.py regards reading the data from a structured CSV file into memory

This accounts for the step between raw data and storage in the database
"""

class Instance(object):
 
    """
    A data instances given data type headers and the corresponding values. 
    Instances are stored in a dictionary (Instance.Data) where the headers are keys
    """
    Data = {} 
    
    def __init__(self, header, values):
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


def convertXLStoCSV(path):
    """
    Convert all spreadsheets in file 'path' to a csv. Saved file is named w/ concatenation of path & spreadsheet name
    """
    pass
